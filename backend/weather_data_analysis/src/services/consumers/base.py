import os
import logging
from kafka import KafkaConsumer
from kafka.consumer.subscription_state import ConsumerRebalanceListener
from json import loads
from src.config.logging import logger
from datetime import datetime
from ...models.analysis import HourlyWeatherData

# Set log level for kafka
logging.getLogger('kafka').setLevel(logging.WARNING)

class WeatherConsumerRebalanceListener(ConsumerRebalanceListener):
    def __init__(self, consumer):
        self.consumer = consumer

    def on_partitions_revoked(self, revoked):
        logger.info(f"Partitions revoked: {revoked}")

    def on_partitions_assigned(self, assigned):
        logger.info(f"Partitions assigned: {assigned}")
        for partition in assigned:
            position = self.consumer.position(partition)
            logger.info(f"Starting position for partition {partition.partition}: {position}")

class BaseWeatherConsumer:
    def __init__(self, bootstrap_servers: str, consumer_type: str):
        self.bootstrap_servers = bootstrap_servers
        worker_id = os.getenv('WORKER_ID', 'default')
        self.group_id = f"{consumer_type}_{worker_id}"
        self.topic = 'weather-mysql.weatherdb.weather_raw_data'
        self._init_consumer()

    def _init_consumer(self):
        try:
            logger.info(f"Bắt đầu khởi tạo consumer với bootstrap servers {self.bootstrap_servers}")
            
            self.consumer = KafkaConsumer(
                self.topic,
                bootstrap_servers=self.bootstrap_servers.split(','),
                group_id=self.group_id,
                auto_offset_reset='earliest',
                enable_auto_commit=False,
                value_deserializer=lambda x: loads(x.decode('utf-8')),
                session_timeout_ms=10000,
                max_poll_interval_ms=600000,
                max_poll_records=2000
            )

            # Create and use the rebalance listener
            self.rebalance_listener = WeatherConsumerRebalanceListener(self.consumer)
            self.consumer.subscribe([self.topic], listener=self.rebalance_listener)
            
            # Check connection
            topics = self.consumer.topics()
            if self.topic not in topics:
                logger.error(f"Topic {self.topic} không tồn tại")
                raise ValueError(f"Topic {self.topic} không tồn tại")
                
            # Log information about partitions
            partitions = self.consumer.partitions_for_topic(self.topic)
            if partitions:
                logger.info(f"Topic {self.topic} có {len(partitions)} partitions")
                
            logger.info(f"Khởi tạo và subscribe thành công consumer với group {self.group_id}")
            
        except Exception as e:
            logger.error(f"Lỗi khởi tạo consumer: {str(e)}", exc_info=True)
            raise

    def _process_message(self, data: dict) -> HourlyWeatherData:
        time = datetime.fromtimestamp(data['time_epoch']).strftime('%Y-%m-%d %H:%M:%S')

        return HourlyWeatherData(
            Id=data['id'],
            TimeEpoch=data['time_epoch'],
            Time=time,
            TempC=data['temp_c'],
            Humidity=data['humidity'],
            PrecipMm=data['precip_mm'],
            WindKph=data['wind_kph'],
            PressureMb=data['pressure_mb'],
            FeelslikeC=data['feelslike_c'],
            WindchillC=data['windchill_c'],
            HeatindexC=data['heatindex_c'],
            DewpointC=data['dewpoint_c'],
            WindDegree=data['wind_degree'],
            WindDir=data['wind_dir'],
        )

    def __del__(self):
        try:
            if hasattr(self, 'consumer'):
                self.consumer.close()
                logger.info(f"Đã đóng consumer group {self.group_id}")
        except Exception as e:
            logger.error(f"Lỗi khi đóng consumer: {str(e)}")