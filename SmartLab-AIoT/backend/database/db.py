"""
数据库模块 - 传感器数据存储与查询

功能概述：
负责所有数据库相关操作，包括数据模型定义、增删改查功能。

数据库类型：
- 默认：SQLite（轻量级文件数据库，适合开发和小规模部署）
- 可选：SQL Server（企业级数据库，适合生产环境）
- 配置：通过 .env 文件的 DB_TYPE 参数切换

数据表结构：
1. sensor_data - 传感器数据表
   - 存储温度、湿度、光照等传感器读数
   - 每条记录包含设备 ID、传感器类型、数值、时间戳

2. alarm_log - 告警日志表
   - 记录温度/湿度异常告警
   - 包含告警类型、告警信息、发生时间

3. device_status - 设备状态表
   - 记录设备在线/离线状态
   - 记录最后在线时间

主要函数：
- save_sensor_data(data) - 保存传感器数据
- get_sensor_data(device_id, limit) - 查询传感器历史数据
- save_alarm_log(device_id, alarm_type, message) - 记录告警
- update_device_status(device_id, status) - 更新设备在线状态

使用示例：
from database.db import save_sensor_data, get_sensor_data

# 保存数据
save_sensor_data(SensorData(device_id="esp32-001", temperature=25.5))

# 查询数据
records = get_sensor_data(device_id="esp32-001", limit=100)
"""
import os
from sqlalchemy import create_engine, Column, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dotenv import load_dotenv

# 加载环境变量（从 .env 文件读取数据库配置）
load_dotenv()

# 创建 SQLAlchemy 模型基类（所有数据表模型都要继承它）
Base = declarative_base()

class SensorData(Base):
    """
    传感器数据表模型
    
    对应数据库表：sensor_data
    用途：存储 IoT 设备上报的传感器读数（温度、湿度、光照等）
    """
    __tablename__ = "sensor_data"

    id = Column(String(100), primary_key=True)         # 主键 ID（设备 ID_ 时间戳）
    device_id = Column(String(50))                     # 设备唯一标识（如：esp32-001）
    temperature = Column(Float)                        # 温度值（℃）
    humidity = Column(Float)                           # 湿度值（%）
    light = Column(Float)                              # 光照值（lux）
    window_open = Column(Boolean, default=False)       # 窗户状态（True=打开，False=关闭）
    timestamp = Column(DateTime, default=datetime.now) # 数据记录时间

class AlarmLog(Base):
    """
    告警日志表模型
    
    对应数据库表：alarm_log
    用途：记录传感器异常告警（温度过高/过低、湿度过高/过低）
    
    告警触发条件（在 main.py 中定义）：
    - 温度 > 35℃ 或 < 15℃
    - 湿度 > 80% 或 < 20%
    """
    __tablename__ = "alarm_log"
    
    id = Column(String(100), primary_key=True)      # 主键 ID（alarm_ 时间戳）
    device_id = Column(String(50))                  # 触发告警的设备 ID
    alarm_type = Column(String(50))                 # 告警类型（如：temperature_high）
    alarm_message = Column(String(255))             # 告警详细信息（如：温度过高：36℃）
    create_time = Column(DateTime, default=datetime.now)  # 告警发生时间

class DeviceStatus(Base):
    """
    设备状态表模型
    
    对应数据库表：device_status
    用途：记录 IoT 设备的在线状态和最后在线时间
    
    使用场景：
    - 设备发送心跳包时更新状态为 "online"
    - 前端页面显示设备是否在线
    """
    __tablename__ = "device_status"
    
    id = Column(String(100), primary_key=True)      # 主键 ID（device_ 设备 ID）
    device_id = Column(String(50))                  # 设备唯一标识
    online_status = Column(String(20))              # 在线状态（"online" / "offline"）
    last_online = Column(DateTime)                  # 最后在线时间

def get_db_url():
    """
    根据环境变量生成数据库连接 URL
    
    支持的数据库类型：
    - SQLite: 文件数据库，无需配置服务器
    - SQL Server: 企业级数据库，需要配置服务器地址和认证信息
    
    配置优先级：
    1. 从 .env 文件读取配置
    2. 如果没有配置，使用默认值（SQLite）
    
    Returns:
        str: 数据库连接 URL
    """
    db_type = os.getenv("DB_TYPE", "sqlite")
    
    if db_type == "sqlserver":
        server = os.getenv("DB_SERVER", ".")
        database = os.getenv("DB_NAME", "SmartLabDB")
        auth_type = os.getenv("DB_AUTH", "windows")
        driver = os.getenv("DB_DRIVER", "ODBC+Driver+17+for+SQL+Server")
        
        if auth_type == "windows":
            return f"mssql+pyodbc://{server}/{database}?driver={driver}&Trusted_Connection=yes"
        else:
            username = os.getenv("DB_USER", "sa")
            password = os.getenv("DB_PASSWORD", "")
            return f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}"
    else:
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))
        db_path = os.path.abspath(os.path.join(BASE_DIR, "../../data/smartlab.db"))
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        return f"sqlite:///{db_path}"

engine = create_engine(get_db_url(), echo=False)  # 创建数据库引擎（echo=False 表示不打印 SQL 语句）
Base.metadata.create_all(engine)  # 自动创建所有数据表（如果不存在）
SessionLocal = sessionmaker(bind=engine)  # 创建数据库会话工厂（用于获取数据库连接）

print(f"Database connected: {get_db_url()}")  # 打印数据库连接信息（启动时显示）

def save_sensor_data(data):
    """
    保存传感器数据到数据库
    
    参数:
        data: SensorData 对象（包含设备 ID、温度、湿度、光照等）
    
    返回:
        bool: 保存成功返回 True，失败返回 False
    
    使用示例:
        data = SensorData(device_id="esp32-001", temperature=25.5, humidity=60)
        save_sensor_data(data)
    """
    db = SessionLocal()
    try:
        record = SensorData(
            id=f"{data.device_id}_{int(datetime.now().timestamp())}",
            device_id=data.device_id,
            temperature=data.temperature if hasattr(data, 'temperature') else None,
            humidity=data.humidity if hasattr(data, 'humidity') else None,
            light=data.light if hasattr(data, 'light') else None,
            window_open=data.window_open if hasattr(data, 'window_open') else None,
            timestamp=datetime.now()
        )
        db.add(record)
        db.commit()
        return True
    except Exception as e:
        print(f"数据库保存失败：{e}")
        db.rollback()
        return False
    finally:
        db.close()

def get_sensor_data(device_id=None, limit=100):
    """
    查询传感器历史数据
    
    参数:
        device_id: 设备 ID（可选，不传则查询所有设备）
        limit: 返回记录数量上限（默认 100 条）
    
    返回:
        list: SensorData 对象列表，按时间倒序排列
    
    使用示例:
        # 查询所有设备的最近 100 条数据
        records = get_sensor_data()
        
        # 查询特定设备的最近 50 条数据
        records = get_sensor_data(device_id="esp32-001", limit=50)
    """
    db = SessionLocal()
    try:
        query = db.query(SensorData)
        if device_id:
            query = query.filter(SensorData.device_id == device_id)
        return query.order_by(SensorData.timestamp.desc()).limit(limit).all()
    finally:
        db.close()

def save_alarm_log(device_id, alarm_type, alarm_message):
    """
    保存告警日志到数据库
    
    参数:
        device_id: 触发告警的设备 ID
        alarm_type: 告警类型（如：temperature_high, humidity_low）
        alarm_message: 告警详细信息（如：温度过高：36℃）
    
    返回:
        bool: 保存成功返回 True，失败返回 False
    
    使用示例:
        save_alarm_log("esp32-001", "temperature_high", "温度过高：36℃")
    """
    db = SessionLocal()
    try:
        record = AlarmLog(
            id=f"alarm_{int(datetime.now().timestamp())}",
            device_id=device_id,
            alarm_type=alarm_type,
            alarm_message=alarm_message,
            create_time=datetime.now()
        )
        db.add(record)
        db.commit()
        return True
    except Exception as e:
        print(f"告警保存失败：{e}")
        db.rollback()
        return False
    finally:
        db.close()

def update_device_status(device_id, online_status):
    """
    更新设备在线状态
    
    参数:
        device_id: 设备 ID
        online_status: 在线状态（"online" / "offline"）
    
    返回:
        bool: 更新成功返回 True，失败返回 False
    
    使用场景:
        - 设备发送心跳包时调用，更新为 "online"
        - 设备长时间无响应时调用，更新为 "offline"
    
    使用示例:
        update_device_status("esp32-001", "online")
    """
    db = SessionLocal()
    try:
        existing = db.query(DeviceStatus).filter(DeviceStatus.device_id == device_id).first()
        if existing:
            # 设备记录已存在，更新状态和时间
            existing.online_status = online_status
            existing.last_online = datetime.now()
        else:
            # 设备记录不存在，创建新记录
            new_status = DeviceStatus(
                id=f"device_{device_id}",
                device_id=device_id,
                online_status=online_status,
                last_online=datetime.now()
            )
            db.add(new_status)
        db.commit()
        return True
    except Exception as e:
        print(f"设备状态更新失败：{e}")
        db.rollback()
        return False
    finally:
        db.close()