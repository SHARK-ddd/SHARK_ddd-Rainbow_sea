import paho.mqtt.client as mqtt
import time
import json

# MQTT配置
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "lab/device/data"
MQTT_HEARTBEAT_TOPIC = "lab/device/heartbeat"

# 模拟设备ID
DEVICE_ID = "test_device_01"

# 连接回调
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("已连接到MQTT服务器!")
        # 订阅主题
        client.subscribe(MQTT_TOPIC)
        client.subscribe(MQTT_HEARTBEAT_TOPIC)
    else:
        print(f"连接失败, 返回代码 {rc}")

# 消息回调
def on_message(client, userdata, msg):
    print(f"收到消息: {msg.topic} -> {msg.payload.decode()}")

# 创建MQTT客户端
client = mqtt.Client()

# 设置回调函数
client.on_connect = on_connect
client.on_message = on_message

# 连接MQTT服务器
print("正在连接MQTT服务器...")
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# 启动网络循环
client.loop_start()

# 模拟接收数据
print("开始模拟接收ESP32数据...")
print("按Ctrl+C停止")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("停止测试")
    client.loop_stop()
    client.disconnect()