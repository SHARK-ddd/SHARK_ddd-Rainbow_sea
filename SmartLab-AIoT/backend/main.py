# 导入 FastAPI 框架核心类和 WebSocket 相关功能
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# 导入跨域资源共享中间件，允许前端跨域访问
from fastapi.middleware.cors import CORSMiddleware
# 从 api 模块导入路由配置
from api import router as api_router
# 导入 MQTT 客户端库，用于连接 IoT 消息服务器
import paho.mqtt.client as mqtt
# 导入 JSON 处理库
import json
# 导入多线程支持
import threading
# 导入时间处理库
import time
# 导入日期时间类
from datetime import datetime
# 导入队列数据结构，用于临时缓存数据
from queue import Queue

# 创建 FastAPI 应用实例，设置服务标题为 SmartLab-AIoT API
app = FastAPI(title="SmartLab-AIoT API")

# 配置 CORS 中间件，允许所有来源、方法和请求头访问 API
# 这样前端页面可以跨域调用 API 接口
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有域名访问 API 接口
    allow_methods=["*"],  # 允许所有 HTTP 方法（GET、POST 等）访问 API 接口
    allow_headers=["*"],  # 允许所有请求头访问 API 接口
)

# 将 API 路由注册到应用中，所有接口路径会加上 /api 前缀
app.include_router(api_router, prefix="/api")

# WebSocket 连接管理器类
# 负责管理所有连接到服务器的 WebSocket 客户端
class ConnectionManager:
    def __init__(self):
        # 存储所有活跃的 WebSocket 连接列表
        self.active_connections: list[WebSocket] = []

    # 建立新的 WebSocket 连接
    async def connect(self, websocket: WebSocket):
        # 接受 WebSocket 握手请求
        await websocket.accept()
        # 将新连接添加到活跃连接列表
        self.active_connections.append(websocket)
        print(f"WebSocket client connected. Total: {len(self.active_connections)}")

    # 断开 WebSocket 连接
    def disconnect(self, websocket: WebSocket):
        # 从活跃连接列表中移除断开的连接
        self.active_connections.remove(websocket)
        print(f"WebSocket client disconnected. Total: {len(self.active_connections)}")

    # 广播消息给所有连接的客户端
    async def broadcast(self, message: str):
        # 遍历所有活跃连接
        for connection in self.active_connections:
            try:
                # 发送消息给当前客户端
                await connection.send_text(message)
            except Exception as e:
                # 如果发送失败，记录错误并断开该连接
                print(f"Error broadcasting to client: {e}")
                self.disconnect(connection)

# 创建全局连接管理器实例
manager = ConnectionManager()

# 健康检查接口
# 用于监控服务是否正常运行
@app.get("/health")
def health():
    # 返回服务状态、名称和当前 WebSocket 连接数
    return {"status": "ok", "service": "smartlab-backend", "websocket_clients": len(manager.active_connections)}

# WebSocket 端点处理函数
# 当客户端连接到 /ws 路径时，会调用这个函数
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # 建立连接
    await manager.connect(websocket)
    try:
        # 持续监听客户端消息（死循环）
        while True:
            # 接收客户端发送的文本消息
            data = await websocket.receive_text()
            print(f"Received from WebSocket: {data}")
    except WebSocketDisconnect:
        # 当客户端断开连接时，清理连接记录
        manager.disconnect(websocket)

# MQTT 服务器配置
# MQTT 是 IoT 设备常用的轻量级消息协议
MQTT_BROKER = "localhost"  # MQTT 服务器地址（本地）
MQTT_PORT = 1883           # MQTT 默认端口

# MQTT 订阅的主题列表
# 每个元组包含 (主题名，QoS 质量等级)
MQTT_TOPICS = [
    ("lab/device/data", 0),      # 设备上报的传感器数据
    ("lab/device/heartbeat", 0), # 设备心跳信号（设备在线状态）
    ("lab/device/alarm", 0)      # 设备主动上报的警报
]

# 告警阈值配置
# 用于判断传感器数据是否异常
ALARM_THRESHOLDS = {
    "temperature_high": 35.0,  # 温度过高阈值（℃）
    "temperature_low": 15.0,   # 温度过低阈值（℃）
    "humidity_high": 80.0,     # 湿度过高阈值（%）
    "humidity_low": 20.0       # 湿度过低阈值（%）
}

# 批量插入数据库的配置
BATCH_INSERT_INTERVAL = 30  # 批量插入时间间隔（秒）
MAX_QUEUE_SIZE = 1000       # 数据队列最大容量
# 创建队列用于临时缓存传感器数据
sensor_data_queue = Queue(maxsize=MAX_QUEUE_SIZE)

# 检查数据是否触发告警的函数
# 根据预设的阈值判断温度、湿度是否异常
def check_alarm(data):
    alarms = []  # 存储告警信息列表
    
    # 检查温度数据
    if "temperature" in data:
        temp = data["temperature"]
        # 温度过高告警
        if temp > ALARM_THRESHOLDS["temperature_high"]:
            alarms.append({"type": "temperature_high", "message": f"温度过高：{temp}℃"})
        # 温度过低告警
        elif temp < ALARM_THRESHOLDS["temperature_low"]:
            alarms.append({"type": "temperature_low", "message": f"温度过低：{temp}℃"})
    
    # 检查湿度数据
    if "humidity" in data:
        humidity = data["humidity"]
        # 湿度过高告警
        if humidity > ALARM_THRESHOLDS["humidity_high"]:
            alarms.append({"type": "humidity_high", "message": f"湿度过高：{humidity}%"})
        # 湿度过低告警
        elif humidity < ALARM_THRESHOLDS["humidity_low"]:
            alarms.append({"type": "humidity_low", "message": f"湿度过低：{humidity}%"})
    
    return alarms  # 返回告警列表

# 批量插入工作线程函数
# 每隔固定时间将队列中的数据批量写入数据库
def batch_insert_worker():
    """定时批量插入数据库的工作线程"""
    print(f"Batch insert worker started, interval: {BATCH_INSERT_INTERVAL} seconds")
    
    # 无限循环，持续处理数据
    while True:
        # 等待指定的时间间隔
        time.sleep(BATCH_INSERT_INTERVAL)
        
        # 如果队列为空，跳过本次循环
        if sensor_data_queue.empty():
            continue
        
        # 从队列中取出所有数据组成批次
        batch_data = []
        while not sensor_data_queue.empty():
            try:
                batch_data.append(sensor_data_queue.get_nowait())
            except:
                break
        
        # 如果批次数据不为空，执行批量插入
        if batch_data:
            insert_batch_to_db(batch_data)
            print(f"Batch inserted {len(batch_data)} records to database")

# 批量插入数据到数据库的函数
# 将一批传感器数据一次性写入数据库，提高效率
def insert_batch_to_db(batch_data):
    """批量插入数据到数据库"""
    db = None
    try:
        # 从数据库模块导入会话类和模型类
        from database.db import SessionLocal, SensorData
        
        # 创建数据库会话
        db = SessionLocal()
        records = []  # 存储要插入的记录列表
        
        # 遍历批次中的每条数据
        for data in batch_data:
            # 创建传感器数据模型实例
            record = SensorData(
                # 生成唯一 ID：设备 ID_ 时间戳_ 序号
                id=f"{data['device_id']}_{int(time.time() * 1000)}_{len(records)}",
                device_id=data['device_id'],           # 设备 ID
                temperature=data.get('temperature'),   # 温度值
                humidity=data.get('humidity'),         # 湿度值
                light=data.get('light'),               # 光照值
                window_open=data.get('window_open'),   # 窗户状态
                # 转换时间戳为 datetime 对象
                timestamp=datetime.fromisoformat(data['timestamp']) if isinstance(data.get('timestamp'), str) else datetime.now()
            )
            records.append(record)
        
        # 批量添加所有记录到数据库
        db.add_all(records)
        # 提交事务
        db.commit()
        return True
    except Exception as e:
        # 如果发生错误，记录错误信息
        print(f"Batch insert failed: {e}")
        if db:
            try:
                # 回滚事务
                db.rollback()
            except:
                pass
        return False
    finally:
        # 确保数据库连接被关闭
        if db:
            db.close()

# MQTT 连接成功时的回调函数
def on_mqtt_connect(client, userdata, flags, rc):
    print(f"MQTT connected with result code {rc}")
    # 订阅所有配置的主题
    client.subscribe(MQTT_TOPICS)

# MQTT 收到消息时的回调函数
# 这是 MQTT 客户端最重要的处理函数
def on_mqtt_message(client, userdata, msg):
    try:
        # 解码消息 payload
        payload = msg.payload.decode('utf-8')
        print(f"MQTT message received: {msg.topic} -> {payload}")
        
        # 处理传感器数据消息
        if msg.topic == "lab/device/data":
            # 解析 JSON 数据
            data = json.loads(payload)
            data['topic'] = msg.topic  # 添加主题信息
            data['timestamp'] = datetime.now().isoformat()  # 添加时间戳
            
            # 通过 WebSocket 广播给所有客户端（实时推送）
            loop = asyncio.get_event_loop()
            loop.call_soon_threadsafe(
                asyncio.create_task,
                manager.broadcast(json.dumps(data))
            )
            
            # 将数据加入队列，等待批量存储
            if sensor_data_queue.qsize() < MAX_QUEUE_SIZE:
                sensor_data_queue.put({
                    'device_id': data.get('device_id', 'unknown'),
                    'temperature': data.get('temperature'),
                    'humidity': data.get('humidity'),
                    'light': data.get('light'),
                    'window_open': data.get('window_open'),
                    'timestamp': data.get('timestamp')
                })
            else:
                print("Warning: Data queue is full, dropping new data")
            
            # 检查是否触发告警
            alarms = check_alarm(data)
            if alarms:
                from database.db import save_alarm_log
                # 保存每条告警记录
                for alarm in alarms:
                    save_alarm_log(data.get('device_id', 'unknown'), alarm['type'], alarm['message'])
        
        # 处理心跳消息
        elif msg.topic == "lab/device/heartbeat":
            data = json.loads(payload)
            from database.db import update_device_status
            # 更新设备状态为在线
            update_device_status(data.get('device_id', 'unknown'), 'online')
        
        # 处理主动上报的警报
        elif msg.topic == "lab/device/alarm":
            data = json.loads(payload)
            from database.db import save_alarm_log
            # 直接保存警报记录
            save_alarm_log(data.get('device_id', 'unknown'), data.get('type', 'unknown'), data.get('message', ''))
            
    except Exception as e:
        # 记录处理消息时的错误
        print(f"Error processing MQTT message: {e}")

# 启动 MQTT 客户端的函数
# 在独立线程中运行，持续监听 MQTT 消息
def start_mqtt_client():
    # 创建 MQTT 客户端实例
    client = mqtt.Client()
    # 设置连接成功回调
    client.on_connect = on_mqtt_connect
    # 设置收到消息回调
    client.on_message = on_mqtt_message
    
    # 无限循环，确保持续连接
    while True:
        try:
            # 连接到 MQTT 服务器
            client.connect(MQTT_BROKER, MQTT_PORT, 60)
            # 开始消息循环（阻塞式）
            client.loop_forever()
        except Exception as e:
            # 连接失败时，等待 5 秒后重试
            print(f"MQTT connection failed: {e}, retrying in 5 seconds...")
            time.sleep(5)

# 创建并启动 MQTT 监听线程
# daemon=True 表示这是守护线程，主程序退出时会自动结束
mqtt_thread = threading.Thread(target=start_mqtt_client, daemon=True)
mqtt_thread.start()

# 创建并启动批量插入数据库的后台线程
batch_thread = threading.Thread(target=batch_insert_worker, daemon=True)
batch_thread.start()

# 程序主入口
if __name__ == "__main__":
    # 导入 uvicorn 作为 ASGI 服务器
    import uvicorn
    # 启动 FastAPI 服务
    # host="0.0.0.0" 表示监听所有网络接口
    # port=8000 表示服务端口号
    uvicorn.run(app, host="0.0.0.0", port=8000)
