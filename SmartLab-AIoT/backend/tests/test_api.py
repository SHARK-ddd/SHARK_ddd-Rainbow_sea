#!/usr/bin/env python3
"""测试脚本：模拟 ESP32 发送数据到后端"""

import requests
import time
import random

BACKEND_URL = "http://localhost:8000/api/sensor/data"

def send_test_data():
    """发送测试数据"""
    data = {
        "sensor_id": "esp32-001",
        "sensor_type": "light",
        "value": random.randint(100, 3000)
    }

    response = requests.post(BACKEND_URL, json=data)
    print(f"发送: {data} -> {response.json()}")

if __name__ == "__main__":
    print("开始发送测试数据...")
    for i in range(10):
        send_test_data()
        time.sleep(1)
    print("测试完成!")

    # 查询历史数据
    resp = requests.get("http://localhost:8000/api/sensor/data?limit=5")
    print(f"\n最近5条数据: {resp.json()}")