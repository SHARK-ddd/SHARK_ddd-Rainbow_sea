import machine
import time
from machine import Pin, ADC

class SensorManager:
    def __init__(self):
        self.light_sensor = ADC(machine.Pin(3))
        self.light_sensor.atten(ADC.ATTN_11DB)
        try:
            from dht import DHT11
            self.dht11 = DHT11(Pin(4))
            self.dht_available = True
            print("DHT11 驱动初始化成功")
        except ImportError:
            self.dht_available = False
            print("警告：DHT11 内置驱动不可用")

    def read_light_sensor(self):
        try:
            adc_value = self.light_sensor.read()
            light_intensity = 4095 - adc_value
            return light_intensity
        except Exception as e:
            print(f"光敏传感器读取失败: {e}")
            return None

    def read_dht11(self):
        if not self.dht_available:
            return None
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                self.dht11.measure()
                temperature = self.dht11.temperature()
                humidity = self.dht11.humidity()
                if temperature is not None and humidity is not None:
                    return {"temperature": temperature, "humidity": humidity}
            except Exception as e:
                print(f"DHT11读取异常: {e}")
            time.sleep_ms(200)
        return None

    def read_all_sensors(self):
        light = self.read_light_sensor()
        dht_data = self.read_dht11()
        
        result = {"light": light}
        if dht_data:
            result["temperature"] = dht_data["temperature"]
            result["humidity"] = dht_data["humidity"]
        return result

    def get_sensor_data(self):
        max_retries = 3
        for attempt in range(max_retries):
            data = self.read_all_sensors()
            if data["light"] is not None:
                return data
            print(f"传感器读取失败，重试 {attempt + 1}/{max_retries}")
            time.sleep(1)
        print("传感器读取多次失败，返回None")
        return None