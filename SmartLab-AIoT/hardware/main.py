import time
import machine
import ubinascii
import ujson
from wifi import WiFiManager
from mqtt import MQTTManager
from sensor import SensorManager

# 配置信息
WIFI_SSID = "17t"
WIFI_PASSWORD = "19959085578"
MQTT_SERVER = "192.168.255.233"  # 你电脑的WiFi IP地址
MQTT_PORT = 1883
MQTT_TOPIC_DATA = "lab/device/data"
MQTT_TOPIC_HEARTBEAT = "lab/device/heartbeat"

# 生成唯一的设备ID
DEVICE_ID = "esp32_s3_" + ubinascii.hexlify(machine.unique_id()).decode('utf-8')[:4]

class SmartLabDevice:
    def __init__(self):
        self.wifi_manager = WiFiManager(WIFI_SSID, WIFI_PASSWORD)
        self.mqtt_manager = MQTTManager(
            client_id=DEVICE_ID,
            server=MQTT_SERVER,
            port=MQTT_PORT
        )
        self.sensor_manager = SensorManager()
        self.last_heartbeat = 0
        self.last_data_upload = 0

    def connect_wifi(self):
        """连接WiFi"""
        return self.wifi_manager.connect()

    def connect_mqtt(self):
        """连接MQTT"""
        return self.mqtt_manager.connect()

    def reconnect_all(self):
        """重新连接所有服务"""
        print("尝试重新连接所有服务...")
        self.wifi_manager.reconnect()
        self.mqtt_manager.reconnect()

    def send_heartbeat(self):
        """发送心跳消息"""
        current_time = time.time()
        if current_time - self.last_heartbeat >= 30:  # 每30秒发送一次心跳
            heartbeat_data = ujson.dumps({
                "device_id": DEVICE_ID,
                "status": "online"
            })
            self.mqtt_manager.publish(MQTT_TOPIC_HEARTBEAT, heartbeat_data)
            self.last_heartbeat = current_time
            return True
        return False

    def send_sensor_data(self):
        """发送传感器数据"""
        current_time = time.time()
        if current_time - self.last_data_upload >= 5:
            sensor_data = self.sensor_manager.get_sensor_data()
            if sensor_data:
                data_with_id = {
                    "device_id": DEVICE_ID,
                    "light": sensor_data["light"],
                    "timestamp": int(time.time())
                }
                if "temperature" in sensor_data:
                    data_with_id["temperature"] = sensor_data["temperature"]
                if "humidity" in sensor_data:
                    data_with_id["humidity"] = sensor_data["humidity"]
                if "window_open" in sensor_data:
                    data_with_id["window_open"] = sensor_data["window_open"]
                payload = ujson.dumps(data_with_id)
                self.mqtt_manager.publish(MQTT_TOPIC_DATA, payload)
                self.last_data_upload = current_time
                return True
        return False

    def run(self):
        """主运行循环"""
        print(f"设备ID: {DEVICE_ID}")
        print("SmartLab AIoT设备启动...")

        # 初始化连接
        if not self.connect_wifi():
            print("WiFi连接失败，退出")
            return

        if not self.connect_mqtt():
            print("MQTT连接失败，退出")
            return

        print("设备初始化完成，开始运行")

        while True:
            try:
                # 发送心跳
                self.send_heartbeat()

                # 发送传感器数据
                self.send_sensor_data()

                # 检查连接状态
                if not self.wifi_manager.is_connected() or not self.mqtt_manager.connected:
                    print("检测到连接断开，尝试重新连接...")
                    self.reconnect_all()

                # 短暂休眠
                time.sleep(1)

            except Exception as e:
                print(f"运行错误: {e}")
                print("尝试重新连接...")
                self.reconnect_all()
                time.sleep(5)

def main():
    device = SmartLabDevice()
    device.run()

if __name__ == "__main__":
    main()