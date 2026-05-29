from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

class InfluxDBManager:
    def __init__(self):
        self.url = os.getenv("INFLUXDB_URL", "http://localhost:8086")
        self.token = os.getenv("INFLUXDB_TOKEN", "smartlab-token")
        self.org = os.getenv("INFLUXDB_ORG", "smartlab-org")
        self.bucket = os.getenv("INFLUXDB_BUCKET", "smartlab-bucket")
        self.client: Optional[InfluxDBClient] = None
        self.write_api = None
        self.query_api = None
        self._enabled = True  # 是否启用 InfluxDB
        self.connect()

    def connect(self):
        if not self._enabled:
            return
        try:
            self.client = InfluxDBClient(url=self.url, token=self.token, org=self.org, timeout=3000)
            self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
            self.query_api = self.client.query_api()
            # 测试连接
            health = self.client.health()
            if health.status != "pass":
                print(f"InfluxDB health check failed: {health.message}")
                self.client = None
        except Exception as e:
            print(f"InfluxDB connection error: {e}")
            self.client = None

    def is_connected(self):
        return self.client is not None
    
    def write_environment_data(self, sensor_id: str, temperature: float, humidity: float, window_status: bool):
        if not self.is_connected():
            return False
        
        try:
            point = Point("environment") \
                .tag("sensor_id", sensor_id) \
                .field("temperature", temperature) \
                .field("humidity", humidity) \
                .field("window_status", window_status) \
                .time(datetime.utcnow(), WritePrecision.NS)
            
            self.write_api.write(bucket=self.bucket, record=point)
            return True
        except Exception as e:
            print(f"Write data error: {e}")
            return False
    
    def write_generic_data(self, measurement: str, tags: dict, fields: dict):
        if not self.is_connected():
            return False
        
        try:
            point = Point(measurement)
            for key, value in tags.items():
                point = point.tag(key, value)
            for key, value in fields.items():
                point = point.field(key, value)
            point = point.time(datetime.utcnow(), WritePrecision.NS)
            
            self.write_api.write(bucket=self.bucket, record=point)
            return True
        except Exception as e:
            print(f"Write generic data error: {e}")
            return False
    
    def query_data(self, measurement: str, field: str, start_time: str = "-1h"):
        if not self.is_connected():
            return []
        
        try:
            query = f'''
                from(bucket: "{self.bucket}")
                |> range(start: {start_time})
                |> filter(fn: (r) => r._measurement == "{measurement}")
                |> filter(fn: (r) => r._field == "{field}")
            '''
            result = self.query_api.query(query)
            data = []
            for table in result:
                for record in table.records:
                    data.append({
                        "time": record.get_time(),
                        "value": record.get_value(),
                        **record.values
                    })
            return data
        except Exception as e:
            print(f"Query data error: {e}")
            return []
    
    def query_environment_data(self, start_time: str = "-1h"):
        return self.query_data("environment", "temperature", start_time)
    
    def close(self):
        if self.client:
            self.client.close()

influxdb_manager = InfluxDBManager()