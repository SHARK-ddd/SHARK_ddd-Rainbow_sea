import paho.mqtt.client as mqtt
import time

MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_TOPIC = "lab/device/#"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ 已连接到本地 MQTT 服务器")
        print(f"📡 订阅主题: {MQTT_TOPIC}")
        print("⏳ 等待接收 ESP32 数据...")
        print("-" * 50)
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"❌ 连接失败，返回码: {rc}")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode('utf-8')
        print(f"\n📨 收到消息:")
        print(f"   主题: {msg.topic}")
        print(f"   内容: {payload}")
    except Exception as e:
        print(f"❌ 解析消息失败: {e}")

def main():
    print("=" * 50)
    print("MQTT 订阅工具")
    print("=" * 50)
    print(f"连接到: {MQTT_BROKER}:{MQTT_PORT}")
    print()
    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n" + "-" * 50)
        print("👋 用户中断，退出程序")
        client.disconnect()
    except Exception as e:
        print(f"\n❌ 连接异常: {e}")
        print("请检查 Mosquitto 服务是否运行")

if __name__ == "__main__":
    main()