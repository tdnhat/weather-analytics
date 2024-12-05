import traceback
import numpy as np
import pandas as pd
from ..models.clustering import (
    CalculateSeasonProbabilityRequest,
    HourlyWeatherData, 
    Centroids,
    SeasonQuantityData,
    ClusteringResultData
)
from typing import List
from sklearn.cluster import KMeans
from ..config.logging import logger
from sklearn.preprocessing import StandardScaler
from ..services.database_api import DatabaseApiService

class ClusteringWeatherService:
    def __init__(self):
        logger.info("Khởi tạo ClusteringWeatherService")
        self.name = "clustering"
        self.dbapi_service = DatabaseApiService()

    def customize_kmean_label(self, kmean_label, half_year, labels: List[int]):
        if half_year == 'First':
            if kmean_label in labels:
                return labels[0]
            return kmean_label
        else:
            if kmean_label in labels:
                return labels[1]
            return kmean_label
        
    def _get_season_quantity(self, data, season_labels, year) -> SeasonQuantityData:
        spring_quantity = len(data[data['kmean_label'] == season_labels['spring']])
        summer_quantity = len(data[data['kmean_label'] == season_labels['summer']])
        autumn_quantity = len(data[data['kmean_label'] == season_labels['autumn']])
        winter_quantity = len(data[data['kmean_label'] == season_labels['winter']])

        return SeasonQuantityData(
            year=year,
            spring_quantity=spring_quantity,
            summer_quantity=summer_quantity,
            autumn_quantity=autumn_quantity,
            winter_quantity=winter_quantity
        )

    async def cluster_daily_data(self, hourly_data: List[HourlyWeatherData]):
        logger.info(f"Bắt đầu phân cụm dữ liệu hàng ngày với {len(hourly_data)} bản ghi")
        
        try:
            # Chuyển dữ liệu từ message -> dataframe
            df = pd.DataFrame([data.model_dump() for data in hourly_data])

            if df.empty:
                raise ValueError("Không có dữ liệu để phân tích")
            
            if df['TempC'].isnull().any():
                logger.warning("Có giá trị null trong dữ liệu")

            df['Time'] = pd.to_datetime(df['Time'])
            df.set_index('Time', inplace=True)

            daily_data = df.resample('D').agg({
                'TempC': 'mean',
            })

            if daily_data.isnull().any().any():
                logger.warning("Có giá trị null trong kết quả phân tích")

            daily_data.columns = ['avg_temp']

            # Reset index to access Time column
            df = df.reset_index()

            # Add colum date based on index column is date type
            daily_data['date'] = daily_data.index

            # ########################################################################################################################
            # Bắt đầu clustering
            features = daily_data[['avg_temp']].to_numpy().reshape(-1, 1)

            # Chuẩn hóa dữ liệu
            scaler = StandardScaler()
            normalized_features = scaler.fit_transform(features)

            # Khởi tạo KMeans
            kmeans = KMeans(n_clusters=4, random_state=42)
            daily_data['kmean_label'] = kmeans.fit_predict(normalized_features)

            logger.info(f"{daily_data}")

            # Lấy labels
            unique_labels = np.unique(kmeans.labels_)

            # Lấy giá trị min và max avg_temp
            min_temp = daily_data['avg_temp'].min()
            max_temp = daily_data['avg_temp'].max()

            # Lấy trường có giá trị avg_temp min và max
            filtered_min_max = daily_data[(daily_data['avg_temp'] == min_temp) | (daily_data['avg_temp'] == max_temp)]

            # Lấy ra 2 label tượng trưng cho nhiệt độ max và min
            summer_winter_labels = np.unique(filtered_min_max['kmean_label'])

            # Xóa 2 label trên, chỉ lấy 2 label ở giữa
            spring_autumn_labels = list(set(unique_labels) - set(summer_winter_labels))
            filtered_labels = [int(x) for x in spring_autumn_labels]

            # Thêm cột half_year
            daily_data['half_year'] = daily_data['date'].dt.month.map(lambda x: 'First' if x <= 6 else 'Second')

            # Điều chỉnh kmean_label dựa vào half_year
            daily_data['kmean_label'] = daily_data.apply(lambda row: self.customize_kmean_label(row['kmean_label'], row['half_year'], labels=filtered_labels), axis=1)

            # Lấy ra số ngày mùa xuân, hạ, thu, đông
            # 1. Lấy ra label mùa hạ (có nhiệt độ cao nhất) - Lấy dựa vào max_temp
            summer_data = daily_data[daily_data['avg_temp'] == max_temp]
            summer_label = summer_data.iloc[0]['kmean_label']
            # 2. Lấy ra label mùa đông (có nhiêt độ thấp nhất) - Lấy dựa vào min_temp
            winter_data = daily_data[daily_data['avg_temp'] == min_temp]
            winter_label = winter_data.iloc[0]['kmean_label']
            # 3. Lấy ra label mùa xuân - dựa vào half_year và spring_autumn_labels
            spring_data = daily_data[(daily_data['half_year'] == 'First') & (daily_data['kmean_label'].isin(spring_autumn_labels))]
            spring_label = spring_data.iloc[0]['kmean_label']
            # 4. Lấy ra label mùa thu - dựa vào half_year và spring_autumn_labels
            autumn_data = daily_data[(daily_data['half_year'] == 'Second') & (daily_data['kmean_label'].isin(spring_autumn_labels))]
            autumn_label = autumn_data.iloc[0]['kmean_label']

            season_labels = {
                "spring": spring_label,
                "summer": summer_label,
                "autumn": autumn_label,
                "winter": winter_label
            }

            # Nhóm dữ liệu lại theo năm
            dailydatas_by_year = {year: group for year, group in daily_data.groupby(daily_data['date'].dt.year)}

            # Tiến hành lấy dữ liệu số lượng mùa xuân, hạ, thu, đông cho từng năm riêng biệt
            season_quantity_result = []
            for year, year_df in dailydatas_by_year.items():
                logger.info(f"Tiến hành lấy dữ liệu từng mùa cho năm {year}")
                result = self._get_season_quantity(data=year_df, season_labels=season_labels, year=year)
                season_quantity_result.append(result)

            logger.info(f"Dữ liệu số lượng mùa sau khi tiến hành phân cụm {season_quantity_result}")

            # ########################################################################################################################
            # Lấy ra centroid cho mùa xuân, hạ, thu, đông
            # Nhận thấy sự tăng dần nhiệt độ max của mùa là sự tăng dần giá trị trong centroids
            # 1. Lấy ra nhiệt độ max của từng mùa
            cluster_temp_ranges = daily_data.groupby('kmean_label')['avg_temp'].agg(['min', 'max']).reset_index()
            # 2. Sắp xếp theo chiều tăng dần của nhiệt độ max
            cluster_temp_ranges = cluster_temp_ranges.sort_values(by='max', ascending=True)
            # 3. Chuyển dữ liệu centroid bị chuẩn hóa về nhiệt độ gốc
            centroids = (scaler.inverse_transform(kmeans.cluster_centers_)).ravel()
            cluster_temp_ranges['centroid'] = np.sort(centroids)

            spring_centroid = cluster_temp_ranges[cluster_temp_ranges['kmean_label'] == spring_label].iloc[0]['centroid']
            summer_centroid = cluster_temp_ranges[cluster_temp_ranges['kmean_label'] == summer_label].iloc[0]['centroid']
            autumn_centroid = cluster_temp_ranges[cluster_temp_ranges['kmean_label'] == autumn_label].iloc[0]['centroid']
            winter_centroid = cluster_temp_ranges[cluster_temp_ranges['kmean_label'] == winter_label].iloc[0]['centroid']

            centroid_result = Centroids(
                spring_centroid=spring_centroid,
                summer_centroid=summer_centroid,
                autumn_centroid=autumn_centroid,
                winter_centroid=winter_centroid
            )

            logger.info(f"Dữ liệu centroids sau khi tiến hành phân cụm {season_quantity_result}")
            # ########################################################################################################################

            result = ClusteringResultData(
                centroids=centroid_result,
                quantity=season_quantity_result
            )

            logger.info(f"Kết quả phân tích: {result.model_dump()}")
            return result

        except Exception as e:
            logger.error(f"Lỗi khi phân cụm hàng ngày: {str(e)}")
            logger.error(f"Chi tiết lỗi: {traceback.format_exc()}")
            raise


    def _calculate_season_probability(self, centroids: Centroids, temperature: float):
        # Tính khoảng cách của nhiệt độ với các centroid tương ứng
        distances = {
            "spring": abs(temperature - centroids.spring_centroid),
            "summer": abs(temperature - centroids.summer_centroid),
            "autumn": abs(temperature - centroids.autumn_centroid),
            "winter": abs(temperature - centroids.winter_centroid),
        }

        # Tính phần trăm
        total_distance = sum(distances.values())
        percentages = {key: round((1 - dist / total_distance) * 100, 2) for key, dist in distances.items()}

        return percentages
