import os
import joblib
import traceback
import numpy as np
import pandas as pd
from ..models.prediction import (
    HourlyWeatherData,
    WeatherData
)
from typing import List
from ..config.logging import logger
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

class WeatherPredictionService:
    def __init__(self):
        logger.info("Khởi tạo WeatherPredictionService")
        self.name = "prediction"

    def _get_data(self, hourly_data_list: List[HourlyWeatherData]):
        df = pd.DataFrame([vars(d) for d in hourly_data_list])
        df['Time'] = pd.to_datetime(df['Time'])
        df.set_index('Time', inplace=True)

        # Resample về ngày
        df_daily = df.resample('D').agg({
            'TempC': 'mean',
            'Humidity': 'mean',
            'WindKph': 'mean',
            'PressureMb': 'mean'
        })

        df_daily.columns = ['avg_temp', 'avg_humidity', 'avg_wind', 'avg_pressure']

        # df_daily['Time'] = pd.to_datetime(df_daily['Time'])
        return df_daily

    def _create_temp_features(self, data):
        logger.info("Tiến hành tạo dữ liệu train cho model nhiệt độ")

        observed_size = 7
        overlap_size = 3
        predict_distance = 1

        features = data[['avg_humidity', 'avg_pressure']].values
        temp_target = data[['avg_temp']].values

        samples = int((len(features) - observed_size) / (observed_size - overlap_size))
        X = np.stack([
            features[i * (observed_size - overlap_size) : i * (observed_size - overlap_size) + observed_size]
            for i in range(samples)
        ])
        y = np.stack([
            temp_target[i * (observed_size - overlap_size) + observed_size + predict_distance - 1]
            for i in range(samples)
        ])

        X = X.reshape(X.shape[0], -1)
        
        return (X,y)
    
    def _create_humidity_features(self, data):
        logger.info("Tiến hành tạo dữ liệu train cho model độ ẩm")

        observed_size = 7
        overlap_size = 5
        predict_distance = 1

        features = data[['avg_temp', 'avg_pressure']].values
        humidity_target = data[['avg_humidity']].values

        samples = int((len(features) - observed_size) / (observed_size - overlap_size))
        X = np.stack([
            features[i * (observed_size - overlap_size) : i * (observed_size - overlap_size) + observed_size]
            for i in range(samples)
        ])
        y = np.stack([
            humidity_target[i * (observed_size - overlap_size) + observed_size + predict_distance - 1]
            for i in range(samples)
        ])

        X = X.reshape(X.shape[0], -1)
        
        return (X,y)
    
    def _create_pressure_features(self, data):
        logger.info("Tiến hành tạo dữ liệu train cho model áp suất khí quyển")

        observed_size = 7
        overlap_size = 3
        predict_distance = 1

        features = data[['avg_temp', 'avg_humidity']].values
        pressure_target = data[['avg_pressure']].values

        samples = int((len(features) - observed_size) / (observed_size - overlap_size))
        X = np.stack([
            features[i * (observed_size - overlap_size) : i * (observed_size - overlap_size) + observed_size]
            for i in range(samples)
        ])
        y = np.stack([
            pressure_target[i * (observed_size - overlap_size) + observed_size + predict_distance - 1]
            for i in range(samples)
        ])

        X = X.reshape(X.shape[0], -1)
        
        return (X,y)

    async def training_model(self, hourly_data: List[HourlyWeatherData]):
        logger.info(f"Bắt đầu train dữ liệu hàng ngày với {len(hourly_data)} bản ghi")
        try:
            daily_data = self._get_data(hourly_data_list=hourly_data)

            # Train model nhiệt độ
            logger.info("Tiến hành train model dự đoán nhiệt độ")
            X_temp, y_temp = self._create_temp_features(daily_data)
            X_temp_train, X_temp_test, y_temp_train, y_temp_test = train_test_split(X_temp, y_temp, test_size=0.3, random_state=42)
            temp_model = RandomForestRegressor(max_depth=2, random_state=0)
            temp_model.fit(X_temp_train, y_temp_train)
            temp_score = temp_model.score(X_temp_test, y_temp_test)
            logger.info(f"Score của mô hình dự đoán nhiệt độ: {temp_score}")

            # Train model độ ẩm
            logger.info("Tiến hành train model dự đoán độ ẩm")
            X_humidity, y_humidity = self._create_humidity_features(daily_data)
            X_humidity_train, X_humidity_test, y_humidity_train, y_humidity_test = train_test_split(X_humidity, y_humidity, test_size=0.3, random_state=42)
            humidity_model = RandomForestRegressor(max_depth=2, random_state=0)
            humidity_model.fit(X_humidity_train, y_humidity_train)
            humidity_score = humidity_model.score(X_humidity_test, y_humidity_test)
            logger.info(f"Score của mô hình dự đoán độ ẩm: {humidity_score}")

            # Train model áp suất khí quyển
            logger.info("Tiến hành train model dự đoán áp suất khí quyển")
            X_pressure, y_pressure = self._create_pressure_features(daily_data)
            X_pressure_train, X_pressure_test, y_pressure_train, y_pressure_test = train_test_split(X_pressure, y_pressure, test_size=0.3, random_state=42)
            pressure_model = RandomForestRegressor(max_depth=2, random_state=0)
            pressure_model.fit(X_pressure_train, y_pressure_train)
            pressure_score = pressure_model.score(X_pressure_test, y_pressure_test)
            logger.info(f"Score của mô hình dự đoán áp suất: {pressure_score}")

            logger.info("Lưu các mô hình...")
            model_dir = os.path.join(os.path.dirname(__file__), '..', 'trained_models')
            os.makedirs(model_dir, exist_ok=True)
            joblib.dump(temp_model, os.path.join(model_dir, 'temp_prediction_model.joblib'))
            joblib.dump(humidity_model, os.path.join(model_dir, 'humidity_prediction_model.joblib'))
            joblib.dump(pressure_model, os.path.join(model_dir, 'pressure_prediction_model.joblib'))

            logger.info("Hoàn thành quá trình training model dự đoán!!!")

            return {
                'temperature_score': temp_score,
                'humidity_score': humidity_score,
                'pressure_score': pressure_score,
            }
        except Exception as e:
            logger.error(f"Lỗi khi phân cụm hàng ngày: {str(e)}")
            logger.error(f"Chi tiết lỗi: {traceback.format_exc()}")
            raise

    def predict_tomorrow(self, data: List[WeatherData]):
        df = pd.DataFrame([vars(d) for d in data])
        print(df)
        df['time'] = pd.to_datetime(df['time'])
        df.set_index('time', inplace=True)

        if (len(df) < 7):
            raise ValueError(f"Không đủ dữ liệu để dự đoán. Cần ít nhất 7 ngày, hiện có {len(df)} ngày.")

        try:
            # Chuẩn bị dữ liệu để dự đoán nhiệt độ
            temp_features = df[['humidity', 'pressure']].values.reshape(1, -1)
            # Chuẩn bị dữ liệu để dự đoán độ ẩm
            humidity_features = df[['temp', 'pressure']].values.reshape(1, -1)
            # Chuẩn bị dữ liệu để dự đoán áp suất
            pressure_features = df[['temp', 'humidity']].values.reshape(1, -1)

            # Load và sử dụng các model
            model_dir = os.path.join(os.path.dirname(__file__), '..', 'trained_models')
            temp_model = joblib.load(os.path.join(model_dir, 'temp_prediction_model.joblib'))
            humidity_model = joblib.load(os.path.join(model_dir, 'humidity_prediction_model.joblib'))
            pressure_model = joblib.load(os.path.join(model_dir, 'pressure_prediction_model.joblib'))

            # Tiến hành dự đoán
            temp_prediction = temp_model.predict(temp_features)
            humidity_prediction = humidity_model.predict(humidity_features)
            pressure_prediction = pressure_model.predict(pressure_features)

            return {
                'predicted_temperature': float(temp_prediction[0]),
                'predicted_humidity': float(humidity_prediction[0]),
                'predicted_pressure': float(pressure_prediction[0]),
            }
        except Exception as e:
            logger.error(f"Lỗi khi phân cụm hàng ngày: {str(e)}")
            logger.error(f"Chi tiết lỗi: {traceback.format_exc()}")
            raise
