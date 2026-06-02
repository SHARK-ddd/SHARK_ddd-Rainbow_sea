import ubinascii
import ujson
from umqtt.simple import MQTTClient
import time
import socket

class MQTTManager:
    def __init__(self, client_id, server, port=1883, username=None, password=None):
        self.client_id = client_id
        self.server = server
        self.port = port
        self.username = username
        self.password = password
        self.client = None
        self.connected = False

    def connect(self):
        """连接MQTT服务器"""
        try:
            print(f"正在连接MQTT服务器: {self.server}:{self.port}")
            print(f"客户端ID: {self.client_id}")
            
            self.client = MQTTClient(
                client_id=self.client_id,
                server=self.server,
                port=self.port,
                user=self.username,
                password=self.password,
                keepalive=60,
                ssl=False
            )

            self.client.connect()
            self.connected = True
            print("MQTT连接成功!")
            return True
        except OSError as e:
            print(f"MQTT连接失败 - OSError: {e}")
            print(f"错误码: {e.errno}")
            if e.errno == 113:
                print("错误原因: 目标主机拒绝连接，请检查网络和防火墙设置")
            elif e.errno == 110:
                print("错误原因: 连接超时，请检查网络连通性")
            self.connected = False
            return False
        except Exception as e:
            print(f"MQTT连接失败 - 未知错误: {type(e).__name__}: {e}")
            self.connected = False
            return False

    def publish(self, topic, payload):
        """发布消息"""
        if not self.connected:
            print("MQTT未连接，无法发布消息")
            return False

        try:
            self.client.publish(topic, payload)
            print(f"发布消息到 {topic}: {payload}")
            return True
        except Exception as e:
            print(f"发布消息失败: {e}")
            self.connected = False
            return False

    def disconnect(self):
        """断开MQTT连接"""
        if self.client:
            self.client.disconnect()
            self.connected = False
            print("MQTT断开连接")

    def reconnect(self):
        """重新连接MQTT"""
        print("尝试重新连接MQTT...")
        self.disconnect()
        return self.connect()