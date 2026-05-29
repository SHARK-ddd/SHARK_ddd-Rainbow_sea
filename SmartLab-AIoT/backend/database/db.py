import os
from sqlalchemy import create_engine, Column, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(String, primary_key=True)
    sensor_id = Column(String)
    sensor_type = Column(String)
    value = Column(Float)
    timestamp = Column(DateTime, default=datetime.now)

# 创建数据库 (使用绝对路径)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.abspath(os.path.join(BASE_DIR, "../../data/smartlab.db"))
os.makedirs(os.path.dirname(db_path), exist_ok=True)
engine = create_engine(f"sqlite:///{db_path}", echo=False)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

print(f"Database path: {db_path}")

def save_sensor_data(data):
    db = SessionLocal()
    try:
        record = SensorData(
            id=f"{data.sensor_id}_{int(datetime.now().timestamp())}",
            sensor_id=data.sensor_id,
            sensor_type=data.sensor_type,
            value=data.value,
            timestamp=datetime.fromisoformat(data.timestamp) if isinstance(data.timestamp, str) else data.timestamp
        )
        db.add(record)
        db.commit()
        return True
    except Exception as e:
        print(f"数据库保存失败: {e}")
        return False
    finally:
        db.close()

def get_sensor_data(sensor_id=None, sensor_type=None, limit=100):
    db = SessionLocal()
    try:
        query = db.query(SensorData)
        if sensor_id:
            query = query.filter(SensorData.sensor_id == sensor_id)
        if sensor_type:
            query = query.filter(SensorData.sensor_type == sensor_type)
        return query.order_by(SensorData.timestamp.desc()).limit(limit).all()
    finally:
        db.close()