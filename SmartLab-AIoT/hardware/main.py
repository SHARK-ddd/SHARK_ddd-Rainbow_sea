# ESP32 MicroPython 主程序
# 先用 Thonny 烧录 MicroPython 固件后运行

import network
import time
from machine import ADC, Pin
import urequests
import ujson

# ===== WiFi 配置 =====
WIFI_SSID = "你的WiFi名称"      # 修改为你的WiFi名称
WIFI_PASSWORD = "你的WiFi密码"  # 修改为你的WiFi密码

# ===== 后端配置 =====
# 修改为你的电脑IP地址 (Windows 运行 ipconfig 查看)
BACKEND_URL = "http://192.168.1.100:8000/api/sensor/data"

# ===== 光敏传感器配置 =====
# 光敏模块接 GPIO34 (ADC1_CH6)
light_sensor = ADC(Pin(34))
light_sensor.atten(ADC.ATTN_11DB)  # 0-4095 范围

def connect_wifi():
    """连接 WiFi"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print(f"正在连接 WiFi: {WIFI_SSID}...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)

        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
            print(".", end="")

    if wlan.isconnected():
        print(f"\nWiFi 连接成功!")
        print(f"IP 地址: {wlan.ifconfig()[0]}")
        return wlan.ifconfig()[0]
    else:
        print("\nWiFi 连接失败!")
        return None

def send_sensor_data(sensor_type, value):
    """发送传感器数据到后端"""
    data = {
        "sensor_id": "esp32-001",
        "sensor_type": sensor_type,
        "value": float(value)
    }

    try:
        response = urequests.post(
            BACKEND_URL,
            data=ujson.dumps(data),
            headers={"Content-Type": "application/json"}
        )
        print(f"发送成功: {response.text}")
        response.close()
    except Exception as e:
        print(f"发送失败: {e}")

def main():
    """主程序"""
    ip = connect_wifi()
    if not ip:
        return

    print("开始采集光敏数据...")

    while True:
        value = light_sensor.read()
        print(f"光敏值: {value}")

        send_sensor_data("light", value)

        time.sleep(5)  # 每5秒采集一次

if __name__ == "__main__":
    main()