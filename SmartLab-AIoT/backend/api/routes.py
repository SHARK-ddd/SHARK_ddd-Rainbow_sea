"""
API 路由模块 - 传感器数据接口定义

功能概述：
提供 RESTful API 接口，用于接收和查询传感器数据。

主要功能：
1. POST /api/sensor/data - 接收传感器上报的数据
2. GET /api/sensor/data - 查询传感器历史数据（支持筛选和分页）

数据模型：
- SensorData: 传感器数据请求模型（设备上报用）
- SensorResponse: 传感器数据响应模型（返回给客户端用）

使用场景：
- IoT 设备通过 POST 接口上报温度、湿度、光照等数据
- 前端页面通过 GET 接口查询历史数据并展示

接口示例：
POST http://localhost:8000/api/sensor/data
  Body: {"sensor_id": "esp32-001", "sensor_type": "temperature", "value": 25.5}

GET http://localhost:8000/api/sensor/data?sensor_id=esp32-001&limit=50
  Response: [{"sensor_id": "esp32-001", "value": 25.5, "timestamp": "..."}]
"""
from fastapi import APIRouter, Query
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

router = APIRouter()

class SensorData(BaseModel):
    """传感器数据请求模型 - 用于接收设备上报的数据"""
    sensor_id: str        # 设备唯一标识（如：esp32-001）
    sensor_type: str      # 传感器类型（如：temperature, humidity, light）
    value: float          # 传感器读数
    timestamp: Optional[str] = None  # 时间戳（可选，默认自动生成）

class SensorResponse(BaseModel):
    """传感器数据响应模型 - 用于返回查询结果"""
    sensor_id: str        # 设备唯一标识
    sensor_type: str      # 传感器类型
    value: float          # 传感器读数
    timestamp: str        # 数据记录时间（ISO 格式）

@router.post("/sensor/data")
def receive_sensor_data(data: SensorData):
    from database.db import save_sensor_data
    data.timestamp = data.timestamp or datetime.now().isoformat()
    save_sensor_data(data)
    print(f"收到数据: {data}")
    return {"status": "received", "data": data}

@router.get("/sensor/data", response_model=List[SensorResponse])
def get_sensor_history(
    sensor_id: Optional[str] = Query(None),
    sensor_type: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000)
):
    from database.db import get_sensor_data
    records = get_sensor_data(sensor_id, sensor_type, limit)
    return [
        SensorResponse(
            sensor_id=r.sensor_id,
            sensor_type=r.sensor_type,
            value=r.value,
            timestamp=r.timestamp.isoformat()
        )
        for r in records
    ]