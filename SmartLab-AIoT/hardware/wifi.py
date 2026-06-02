import network
import time

class WiFiManager:
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
        self.wlan = network.WLAN(network.STA_IF)

    def connect(self):
        """连接WiFi网络"""
        print("正在连接WiFi...")
        self.wlan.active(True)
        self.wlan.connect(self.ssid, self.password)

        # 等待连接
        max_attempts = 20
        for i in range(max_attempts):
            if self.wlan.isconnected():
                print("WiFi连接成功!")
                print("IP地址:", self.wlan.ifconfig()[0])
                return True
            time.sleep(1)
            print(f"连接中... {i+1}/{max_attempts}")

        print("WiFi连接失败!")
        return False

    def is_connected(self):
        """检查是否已连接"""
        return self.wlan.isconnected()

    def reconnect(self):
        """重新连接WiFi"""
        print("尝试重新连接WiFi...")
        self.wlan.disconnect()
        return self.connect()