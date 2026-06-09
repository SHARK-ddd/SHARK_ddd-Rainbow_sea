#!/usr/bin/env python3
"""
API 接口测试脚本 - 模拟 ESP32 设备发送数据

功能概述：
模拟 IoT 设备（如 ESP32 单片机）向后端 API 发送传感器数据，
用于测试后端服务是否正常运行。

测试流程：
1. 模拟 ESP32 设备生成随机传感器数据
2. 通过 POST 请求发送到后端 API
3. 验证响应结果
4. 发送 10 次数据后，查询最近 5 条历史记录

使用方式：
1. 确保后端服务已启动（python main.py）
2. 运行测试脚本：python tests/test_api.py
3. 观察输出结果

依赖库：
- requests: 用于发送 HTTP 请求
"""

import requests
import time
import random

# 后端 API 地址（发送传感器数据的接口）
BACKEND_URL = "http://localhost:8000/api/sensor/data"

def send_test_data():
    """
    发送测试数据到后端 API
    
    模拟数据：
    - sensor_id: 设备编号（esp32-001）
    - sensor_type: 传感器类型（light 光照传感器）
    - value: 随机光照值（100-3000 lux）
    """
    data = {
        "sensor_id": "esp32-001",      # 设备 ID
        "sensor_type": "light",         # 传感器类型
        "value": random.randint(100, 3000)  # 随机光照值
    }

    # 发送 POST 请求
    response = requests.post(BACKEND_URL, json=data)
    print(f"发送：{data} -> {response.json()}")

if __name__ == "__main__":
    print("开始发送测试数据...")
    
    # 循环发送 10 次数据，每次间隔 1 秒
    for i in range(10):
        send_test_data()
        time.sleep(1)
    
    print("测试完成!")

    # 查询历史数据（验证数据是否成功存储）
    resp = requests.get("http://localhost:8000/api/sensor/data?limit=5")
    print(f"\n最近 5 条数据：{resp.json()}")
