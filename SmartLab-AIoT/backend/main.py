from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from api import router as api_router
import paho.mqtt.client as mqtt
import json
import threading
import time

app = FastAPI(title="SmartLab-AIoT API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"WebSocket client connected. Total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f"WebSocket client disconnected. Total: {len(self.active_connections)}")

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"Error broadcasting to client: {e}")
                self.disconnect(connection)

manager = ConnectionManager()

@app.get("/health")
def health():
    return {"status": "ok", "service": "smartlab-backend", "websocket_clients": len(manager.active_connections)}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received from WebSocket: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPICS = [
    ("lab/device/data", 0),
    ("lab/device/heartbeat", 0),
    ("lab/device/alarm", 0)
]

def on_mqtt_connect(client, userdata, flags, rc):
    print(f"MQTT connected with result code {rc}")
    client.subscribe(MQTT_TOPICS)

def on_mqtt_message(client, userdata, msg):
    try:
        payload = msg.payload.decode('utf-8')
        print(f"MQTT message received: {msg.topic} -> {payload}")
        
        if msg.topic == "lab/device/data":
            data = json.loads(payload)
            data['topic'] = msg.topic
            
            import asyncio
            asyncio.run(manager.broadcast(json.dumps(data)))
            
            from database.db import save_sensor_data
            class SensorData:
                def __init__(self, data):
                    self.sensor_id = data.get('device_id', 'unknown')
                    self.sensor_type = 'environment'
                    self.value = data.get('temperature', 0)
                    self.timestamp = time.strftime('%Y-%m-%dT%H:%M:%S')
            
            save_sensor_data(SensorData(data))
            
        elif msg.topic == "lab/device/heartbeat":
            pass
            
    except Exception as e:
        print(f"Error processing MQTT message: {e}")

def start_mqtt_client():
    client = mqtt.Client()
    client.on_connect = on_mqtt_connect
    client.on_message = on_mqtt_message
    
    while True:
        try:
            client.connect(MQTT_BROKER, MQTT_PORT, 60)
            client.loop_forever()
        except Exception as e:
            print(f"MQTT connection failed: {e}, retrying in 5 seconds...")
            time.sleep(5)

mqtt_thread = threading.Thread(target=start_mqtt_client, daemon=True)
mqtt_thread.start()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)