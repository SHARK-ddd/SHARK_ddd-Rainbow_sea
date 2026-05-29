from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

router = APIRouter()

class SensorData(BaseModel):
    sensor_id: str
    sensor_type: str
    value: float
    timestamp: Optional[str] = None

class SensorResponse(BaseModel):
    sensor_id: str
    sensor_type: str
    value: float
    timestamp: str

class EnvironmentData(BaseModel):
    sensor_id: str
    temperature: float
    humidity: float
    window_status: bool

class GenericDataPoint(BaseModel):
    measurement: str
    tags: dict
    fields: dict

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

@router.post("/influxdb/environment")
def write_environment_data(data: EnvironmentData):
    from utils.influxdb_utils import influxdb_manager
    
    success = influxdb_manager.write_environment_data(
        sensor_id=data.sensor_id,
        temperature=data.temperature,
        humidity=data.humidity,
        window_status=data.window_status
    )
    
    if success:
        return {"status": "success", "message": "数据写入成功"}
    else:
        raise HTTPException(status_code=500, detail="InfluxDB写入失败")

@router.post("/influxdb/write")
def write_generic_data(data: GenericDataPoint):
    from utils.influxdb_utils import influxdb_manager
    
    success = influxdb_manager.write_generic_data(
        measurement=data.measurement,
        tags=data.tags,
        fields=data.fields
    )
    
    if success:
        return {"status": "success", "message": "数据写入成功"}
    else:
        raise HTTPException(status_code=500, detail="InfluxDB写入失败")

@router.get("/influxdb/query")
def query_influxdb_data(
    measurement: str,
    field: str,
    start_time: str = Query("-1h")
):
    from utils.influxdb_utils import influxdb_manager
    
    data = influxdb_manager.query_data(
        measurement=measurement,
        field=field,
        start_time=start_time
    )
    
    return {"status": "success", "data": data}

@router.get("/influxdb/environment")
def get_environment_data(
    start_time: str = Query("-1h")
):
    from utils.influxdb_utils import influxdb_manager
    
    data = influxdb_manager.query_environment_data(start_time=start_time)
    
    return {"status": "success", "data": data}

@router.get("/influxdb/health")
def check_influxdb_connection():
    from utils.influxdb_utils import influxdb_manager
    
    if influxdb_manager.is_connected():
        return {"status": "connected", "message": "InfluxDB连接正常"}
    else:
        return {"status": "disconnected", "message": "InfluxDB连接失败"}