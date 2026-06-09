# SmartLab-AIoT 技术架构文档

***

## 一、项目概述

### 1.1 项目定位

**SmartLab-AIoT** 是一个基于 ESP32-S3 的智慧实验室环境监测系统，实现从传感器数据采集到 Web 实时可视化的完整闭环。

### 1.2 核心目标

| 目标             | 描述                        |
| -------------- | ------------------------- |
| 环境数据实时采集     | ESP32传感器节点采集温湿度、光照、门窗状态    |
| MQTT云端通信     | 可靠的物联网消息传输协议              |
| FastAPI后端处理  | 高性能数据处理服务                 |
| WebSocket实时推送 | 毫秒级数据更新到前端                |
| Web可视化管理     | 现代化深色科技风 Dashboard         |

### 1.3 项目状态

- **当前版本**: v1.0
- **项目状态**: ✅ 活跃开发中
- **最后更新**: 2026年6月

***

## 二、技术栈

### 2.1 硬件层

| 组件      | 技术               | 说明                    |
| ------- | ---------------- | --------------------- |
| 主控芯片    | ESP32-S3-N16R8   | MicroPython 固件        |
| 温湿度传感器  | DHT11            | GPIO4（内置驱动）          |
| 光照传感器   | 光敏电阻             | GPIO3（ADC 模拟读取）        |
| 门窗传感器   | 干簧开关             | GPIO10（数字读取，下拉电阻）    |
| 通信模块    | WiFi 802.11b/g/n | 网络通信                  |

### 2.2 后端层

| 组件       | 技术            | 版本       |
| -------- | ------------- | -------- |
| 框架       | FastAPI       | 0.136.3  |
| 服务器      | Uvicorn       | 最新       |
| MQTT客户端   | paho-mqtt     | 最新       |
| 数据库      | SQL Server      | 2019+    |
| ORM      | SQLAlchemy    | 最新       |
| 驱动       | pyodbc          | 4.0.35+  |
| 配置       | python-dotenv | 最新       |

### 2.3 前端层

| 组件   | 技术               | 说明     |
| ---- | ---------------- | ------ |
| UI框架 | Bootstrap 5      | 响应式布局  |
| 图表库  | ECharts 5.4      | 数据可视化  |
| 水波图  | echarts-liquidfill | 湿度液态图  |
| 图标   | Font Awesome 6.4 | 图标库    |
| 实时通信 | WebSocket        | 实时推送   |
| 动画效果 | CSS3 Animations  | 交互动效   |

***

## 三、系统架构

### 3.1 架构分层图

```
┌─────────────────────────────────────────────────────────────────┐
│                       Web 前端层                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 实时数值卡片·告警面板·Gauge仪表·LiquidFill·Donut·      │   │
│  │  堆叠柱状图·24h热力图·温度趋势·光照趋势                  │   │
│  │                     ↑ WebSocket 接收                    │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↑ WebSocket
┌─────────────────────────────────────────────────────────────────┐
│                      FastAPI 后端层                              │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   │
│  │ MQTT订阅  │→ │ WebSocket │   │ REST API │   │ 批量插入  │   │
│  │ 实时广播  │   │ 数据推送  │   │ 数据接口  │   │ SQL Server│   │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↑ MQTT
┌─────────────────────────────────────────────────────────────────┐
│                      MQTT Broker                                │
│                  Mosquitto (端口: 1883)                         │
└─────────────────────────────────────────────────────────────────┘
                              ↑ MQTT
┌─────────────────────────────────────────────────────────────────┐
│                      ESP32 硬件层                                │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   │
│  │ DHT11    │   │ 光敏电阻   │   │ 干簧开关   │   │ WiFi     │   │
│  │ 温湿度    │   │ 光照      │   │ 门窗状态   │   │ 网络通信   │   │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 端到端数据流

```
ESP32传感器采集 → MQTT发布(lab/device/data) → Mosquitto Broker
    → FastAPI订阅 → WebSocket广播 → 前端Dashboard实时展示
    → 30秒批量插入 → SQL Server持久化存储
    → 阈值检测 → 告警日志记录
```

***

## 四、项目目录结构

```
SmartLab-AIoT/
├── backend/                 # FastAPI 后端服务
│   ├── api/                 # API 路由层
│   │   ├── routes.py        # REST API 路由
│   │   └── __init__.py
│   ├── database/            # 数据库操作层
│   │   ├── db.py            # SQL Server 操作（SQLAlchemy ORM）
│   │   └── __init__.py
│   ├── main.py              # 应用入口 (MQTT订阅 + WebSocket广播 + 批量入库)
│   ├── requirements.txt     # Python 依赖
│   └── .env.example         # 环境变量示例
├── hardware/                # ESP32 硬件层
│   ├── main.py              # 主程序（WiFi连接 · 数据上报 · 心跳）
│   ├── sensor.py            # 传感器驱动（DHT11 · 光敏电阻 · 干簧开关）
│   ├── mqtt.py              # MQTT 发布客户端
│   ├── wifi.py              # WiFi 连接管理
│   ├── mqtt_subscribe.py    # MQTT 订阅调试
│   ├── mqtt_test.py         # MQTT 功能测试
│   └── start_mosquitto.bat  # MQTT Broker 启动脚本
├── frontend/                # Web 前端
│   └── index.html           # 监测 Dashboard（单文件，含所有图表与样式）
├── docs/                    # 项目文档
│   ├── TECHNICAL_DOCUMENTATION.md
│   ├── project_status.md
│   └── visualization_plan.md
├── data/                    # 运行时数据 (gitignored)
└── start_all.ps1            # 一键启动脚本
```

***

## 五、核心模块实现

### 5.1 后端主程序 ([backend/main.py](file:///e:/graduationProject/SmartLab-AIoT/backend/main.py))

**功能职责**:

- FastAPI 应用初始化，允许跨域请求
- `/health` 健康检查接口（返回在线的 WebSocket 客户端数量）
- `/ws` WebSocket 端点，支持多客户端同时连接
- `ConnectionManager`：管理所有在线 WebSocket 连接，消息广播到所有客户端
- MQTT 订阅线程：独立守护线程，监听 `lab/device/data`、`lab/device/heartbeat`、`lab/device/alarm` 三个主题
- 数据广播机制：MQTT 消息到来后立刻广播到所有 WebSocket 前端
- 告警检测：温度 <15°C / >35°C，湿度 <20% / >80% 触发告警并写入数据库
- **批量插入**：MQTT 消息写入队列，独立线程每 30 秒批量 flush 到 SQL Server（减少 IO 开销，队列上限 1000 条）
- 断线自动重连：MQTT 与 Mosquitto 断开时每 5 秒重试

### 5.2 API 路由层 ([backend/api/routes.py](file:///e:/graduationProject/SmartLab-AIoT/backend/api/routes.py))

| 接口              | 方法   | 描述                             |
| --------------- | ---- | ------------------------------ |
| `/health`       | GET  | 健康检查，返回在线 WebSocket 客户端数          |
| `/api/sensor/data` | POST | 单条传感器数据写入（device_id / sensor_type / value / timestamp） |
| `/api/sensor/data` | GET  | 查询传感器历史（可按 device_id / sensor_type 过滤，默认 limit=100） |

### 5.3 数据库层 ([backend/database/db.py](file:///e:/graduationProject/SmartLab-AIoT/backend/database/db.py))

**数据库引擎**: SQL Server 2019+（通过 pyodbc + SQLAlchemy 连接）

**连接配置**: 通过 `backend/.env` 文件管理（详见第十章）

**数据表结构**（共 3 张表，项目启动时自动创建）:

| 表名            | 字段                                         | 说明              |
| ------------- | ------------------------------------------ | --------------- |
| `sensor_data` | id · device_id · temperature · humidity · light · window_open · timestamp | 传感器原始数据（每30秒批量插入） |
| `alarm_log`   | id · device_id · alarm_type · alarm_message · create_time | 告警日志（温/湿度异常）     |
| `device_status` | id · device_id · online_status · last_online  | 设备在线状态（心跳更新）        |

**数据库特性**:

- SQLAlchemy ORM 管理，支持 SQL Server T-SQL 方言
- 自动建表：`Base.metadata.create_all(engine)` 项目启动时执行
- 连接池管理：`SessionLocal = sessionmaker(bind=engine)`
- 单条/批量写入两种模式：MQTT 线程使用批量 `add_all()`，API 使用单条 `add()`
- 事务回滚：写入异常时自动 `db.rollback()`

### 5.4 ESP32 主程序 ([hardware/main.py](file:///e:/graduationProject/SmartLab-AIoT/hardware/main.py))

**核心功能**:

- 启动时连接 WiFi 与 MQTT Broker（IP 地址由 `MQTT_SERVER` 常量配置）
- 主循环：
  - **每 5 秒**：`SensorManager` 读取全部传感器 → 通过 MQTT Manager 发布到 `lab/device/data`
  - **每 30 秒**：发布心跳消息到 `lab/device/heartbeat`，内容含 `device_id` 与状态 `online`
- 连接守护：WiFi 与 MQTT 任一处断开即进入重连逻辑
- 设备 ID：基于 ESP32 唯一硬件 ID 生成 `esp32_s3_xxxx` 格式

### 5.5 传感器驱动 ([hardware/sensor.py](file:///e:/graduationProject/SmartLab-AIoT/hardware/sensor.py))

| 传感器   | Pin  | 读取方式          | 数值范围             |
| ----- | ---- | ------------- | ---------------- |
| DHT11 | 4    | 内置 `dht` 驱动   | 温度(°C) · 湿度(%)     |
| 光敏电阻  | 3    | ADC 读取（12 位）  | 0 ~ 4095（数值越大光照越强） |
| 干簧开关  | 10   | 数字输入（内部下拉）  | 0 = 关闭 · 1 = 打开       |

- DHT11 失败自动重试 3 次
- 干簧开关用于门窗状态检测
- 失败时返回 `None`，上游主程序会跳过该字段

### 5.6 MQTT 发布客户端 ([hardware/mqtt.py](file:///e:/graduationProject/SmartLab-AIoT/hardware/mqtt.py))

- 基于 MicroPython `umqtt.simple`
- 支持匿名连接（Mosquitto 默认配置）
- 发布 QoS=0，非阻塞
- 主动 `disconnect / reconnect` 方法，配合主循环的异常重连策略

### 5.7 WiFi 连接管理 ([hardware/wifi.py](file:///e:/graduationProject/SmartLab-AIoT/hardware/wifi.py))

- STA 模式启动，连接到配置的 SSID / 密码
- 连接失败返回 `False`，上层负责重试
- 提供 `is_connected()` 状态查询

### 5.8 前端 Dashboard ([frontend/index.html](file:///e:/graduationProject/SmartLab-AIoT/frontend/index.html))

**单文件 Dashboard**（无构建过程，直接浏览器打开即可），采用**深色科技风 + 毛玻璃 + 发光边框**设计。

**可视化组件**:

| 区域     | 组件                   | 说明                          |
| ------ | -------------------- | --------------------------- |
| 顶部导航栏  | Logo · 实时时钟 · 设备ID · WS 状态 | 每秒更新的本地时钟与 WebSocket 连接徽章   |
| 指标卡片行  | 温度 · 湿度 · 光照 · 门窗状态   | 大号数字 + 单位 + 更新时间，按数值着色       |
| 告警面板   | 滚动告警列表               | 支持 severity 等级（danger/warning）   |
| 仪表行    | Gauge · LiquidFill · Donut | 光照仪表盘 · 湿度水波图 · 综合健康度环形图    |
| 对比分析行  | 堆叠柱状图 · 24h 热力图         | 最近 12 条温度/湿度对比 · 24 小时分桶均值热力 |
| 趋势行    | 温度趋势 · 光照趋势            | 折线 + 渐变填充区域，保留最近 60 个数据点    |

**告警规则**（前端实时检测 + 后端阈值记录）:

- 温度：< 15°C 警告 · > 30°C 危险
- 湿度：< 30% 警告 · > 60% 危险
- 光照：< 800 lux 警告 · > 3200 lux 危险

**WebSocket 行为**:

- 启动时连接 `ws://localhost:8000/ws`
- 断线自动每 5 秒重连
- 接收 JSON 消息并触发：数值更新 → 图表 append → 告警检测 → 仪表盘刷新
- 自动响应窗口 resize，所有图表重新布局

***

## 六、MQTT Topic 设计

| Topic                  | QoS | 消息示例                                                                                                                   |
| ---------------------- | --- | ---------------------------------------------------------------------------------------------------------------------- |
| `lab/device/data`      | 0   | `{"device_id":"esp32_s3_abcd","temperature":25.5,"humidity":50,"light":1200,"window_open":0,"timestamp":1718000000}` |
| `lab/device/heartbeat` | 0   | `{"device_id":"esp32_s3_abcd","status":"online"}`                                                                      |
| `lab/device/alarm`     | 0   | `{"device_id":"esp32_s3_abcd","type":"temperature_high","message":"温度过高: 36.5°C"}`                                  |

***

## 七、已完成功能清单

### 7.1 后端功能

| 功能              | 状态 | 说明                                                    |
| --------------- | -- | ----------------------------------------------------- |
| FastAPI 服务框架     | ✅  | 标准 ASGI 应用，CORS 全开放                                |
| MQTT 订阅服务        | ✅  | 独立守护线程，订阅 3 个 topic，断线每 5 秒自动重连                 |
| WebSocket 广播服务    | ✅  | `ConnectionManager` 管理多客户端，MQTT 消息即时推送                 |
| SQL Server 持久化    | ✅  | 3 张表（sensor_data / alarm_log / device_status），自动建表 |
| 批量数据入库          | ✅  | 30 秒周期 + 队列缓冲（上限 1000），大幅减少数据库写 IO           |
| 实时告警检测          | ✅  | 温/湿度阈值检测，异常写入 `alarm_log` 表                          |
| REST API 接口       | ✅  | `POST /api/sensor/data` 与 `GET /api/sensor/data`           |
| 健康检查接口          | ✅  | `/health` 返回服务状态与在线 WS 客户端数                        |
| 设备心跳处理          | ✅  | `lab/device/heartbeat` → 更新 `device_status` 表              |

### 7.2 硬件功能

| 功能         | 状态 | 说明                                      |
| ---------- | -- | --------------------------------------- |
| WiFi 连接管理 | ✅  | STA 模式，连接状态轮询，失败返回 false                 |
| MQTT 发布客户端 | ✅  | `umqtt.simple`，支持匿名发布、断线重连                 |
| DHT11 温湿度  | ✅  | GPIO4，内置驱动，3 次重试                         |
| 光敏电阻采集     | ✅  | GPIO3 ADC 读取，12 位分辨率（0~4095）               |
| 干簧开关（门窗）  | ✅  | GPIO10 数字输入，门/窗开/关状态                       |
| 定时数据上报     | ✅  | 每 5 秒一次 publish                              |
| 心跳检测       | ✅  | 每 30 秒一次 heartbeat                          |
| 异常重连机制     | ✅  | 主循环持续检测 WiFi / MQTT 状态，异常自动 reconnect       |

### 7.3 前端功能

| 功能            | 状态 | 说明                                         |
| ------------- | -- | ------------------------------------------ |
| 实时数值展示        | ✅  | 温度 / 湿度 / 光照 / 门窗 4 个指标卡片                |
| WebSocket 实时连接 | ✅  | `ws://localhost:8000/ws`，自动重连                |
| ECharts 图表     | ✅  | Gauge · LiquidFill · Donut · 堆叠柱状图 · 热力图 · 趋势线 |
| 告警系统          | ✅  | 3 个指标的双阈值判定，告警条目列表，支持一键清除              |
| 深色科技风 UI      | ✅  | 毛玻璃卡片 + 发光边框 + 渐变背景                         |
| 响应式布局         | ✅  | Bootstrap Grid，断点适配桌面/平板/移动端                   |
| 实时时钟与连接状态    | ✅  | 头部始终可见的本地时钟与 ONLINE/OFFLINE 徽章               |

***

## 八、关键技术配置

### 9.1 环境要求

- Python 3.8+
- Mosquitto MQTT Broker（默认端口 1883）
- ESP32 / ESP32-S3 设备 + MicroPython 固件
- 浏览器：Chrome / Edge / Firefox（ES2017+ 以运行 ECharts）

### 9.2 启动步骤

```bash
# 1. 启动 MQTT Broker
# Windows（硬件目录脚本）
SmartLab-AIoT\hardware\start_mosquitto.bat
# Linux
mosquitto -p 1883

# 2. 安装后端依赖
cd SmartLab-AIoT/backend
pip install -r requirements.txt

# 3. 启动后端服务（默认监听 0.0.0.0:8000）
python main.py
# 健康检查: http://localhost:8000/health
# API 文档: http://localhost:8000/docs

# 4. 打开前端
# 直接浏览器打开 frontend/index.html
# 或用任意静态服务器（如: python -m http.server 8080 --directory frontend）
```

### 9.3 ESP32 部署

1. 使用 Thonny 或 `mpremote` 烧录 MicroPython 固件（建议官方 esp32- GENERIC-S3 1.24.x）
2. 上传以下 4 个文件到 ESP32 的文件系统根目录：
   - `wifi.py`
   - `mqtt.py`
   - `sensor.py`
   - `main.py`
3. 修改 `hardware/main.py` 顶部常量：
   - `WIFI_SSID` / `WIFI_PASSWORD`：实验室 WiFi
   - `MQTT_SERVER`：运行后端那台机器的局域网 IP（例如 `192.168.1.100`）
4. 复位启动，串口可见 `设备ID: esp32_s3_xxxx` / `MQTT连接成功` 等日志

***

## 十、技术亮点

### 10.1 实时数据推送

- WebSocket 即时广播，ESP32 上报 → 前端刷新几乎零延迟
- 多前端并发连接：后端 `ConnectionManager` 统一管理
- 前端断线自动每 5 秒重连，后端 MQTT 同样自动重连

### 10.2 低成本硬件

- ESP32-S3 单芯片方案，内置 WiFi + BLE
- 传感器全部使用通用/低成本模块（DHT11、光敏分压、干簧开关），便于 DIY 与替换

### 10.3 现代化可视化

- 深色科技风 UI（毛玻璃 + 发光 + 渐变）
- 7 种不同图表组合（Gauge / LiquidFill / Donut / StackedBar / Heatmap / Line×2）
- 单文件部署，零构建过程，直接浏览器打开即可

### 10.4 健壮性设计

- ESP32 端：WiFi / MQTT 双层异常检测与重连
- 后端端：MQTT 守护线程 + 队列缓冲（上限 1000）+ 30 秒批量入库
- 前端端：WebSocket 心跳重连 + 图表窗口自适应 resize

***

## 十、数据库详解

### 10.1 ESP32 端配置（[hardware/main.py](file:///e:/graduationProject/SmartLab-AIoT/hardware/main.py)）

```python
WIFI_SSID     = "your_wifi_ssid"
WIFI_PASSWORD = "your_wifi_password"
MQTT_SERVER   = "192.168.1.100"   # 后端机器的局域网 IP
MQTT_PORT     = 1883
MQTT_TOPIC_DATA      = "lab/device/data"
MQTT_TOPIC_HEARTBEAT = "lab/device/heartbeat"
```

### 10.2 后端配置（[backend/main.py](file:///e:/graduationProject/SmartLab-AIoT/backend/main.py)）

| 配置项                    | 默认值      | 说明                         |
| ---------------------- | -------- | -------------------------- |
| `MQTT_BROKER`          | localhost | Mosquitto 地址                |
| `MQTT_PORT`            | 1883     | MQTT 端口                    |
| `BATCH_INSERT_INTERVAL` | 30       | 秒，批量入库的周期                 |
| `MAX_QUEUE_SIZE`       | 1000     | 队列缓存上限，超出丢弃                |
| 温度告警阈值                 | 15 / 35  | °C                          |
| 湿度告警阈值                 | 20 / 80  | %                           |

### 10.3 数据库配置（[backend/database/db.py](file:///e:/graduationProject/SmartLab-AIoT/backend/database/db.py)）

**数据库引擎**: SQL Server 2019+（通过 pyodbc + SQLAlchemy 连接）

**连接文件**: `backend/.env`（从 `.env.example` 复制修改）

```ini
# .env 配置示例
DB_TYPE=sqlserver
DB_SERVER=localhost
DB_PORT=1433
DB_NAME=SmartLabDB
DB_USER=sa
DB_PASSWORD=your_password_here
DB_DRIVER=ODBC+Driver+17+for+SQL+Server
DB_AUTH=sqlserver
```

**数据库驱动要求**:

- `pyodbc >= 4.0.35`
- `ODBC Driver 17 for SQL Server`（需单独安装）

**表自动创建**: 项目启动时 `Base.metadata.create_all(engine)` 会自动创建以下三张表，无需手动建表。

---

## 十一、数据库表结构详解

### 11.1 `sensor_data` 表（传感器原始数据）

| 字段名          | 数据类型           | 是否可空 | 主键 | 说明                                |
| --------------- | ------------------ | -------- | ---- | ----------------------------------- |
| `id`            | NVARCHAR(100)      | ❌ NOT NULL | ✅   | 主键，格式 `{device_id}_{时间戳毫秒}_{序号}` |
| `device_id`     | NVARCHAR(50)       | ✅      |      | 设备 ID，如 `esp32_s3_abcd`           |
| `temperature`   | FLOAT              | ✅      |      | 温度值（°C），可为空                     |
| `humidity`      | FLOAT              | ✅      |      | 湿度值（%），可为空                      |
| `light`         | FLOAT              | ✅      |      | 光照强度（ADC 值 0~4095），可为空           |
| `window_open`   | BIT                | ✅      |      | 门窗状态（1=打开，0=关闭），可为空            |
| `timestamp`     | DATETIME           | ✅      |      | 数据记录时间，默认 `GETDATE()`           |

**数据示例**:

```
id                                | device_id      | temperature | humidity | light  | window_open | timestamp
----------------------------------+----------------+-------------+----------+--------+-------------+-------------------
esp32_s3_abcd_1718000000000_0     | esp32_s3_abcd  | 25.5        | 50.0     | 1200.0 | 0           | 2024-06-10 14:30:00
esp32_s3_abcd_1718000030000_0     | esp32_s3_abcd  | 25.6        | 50.2     | 1250.0 | 0           | 2024-06-10 14:30:30
```

**写入方式**: MQTT 订阅线程每 30 秒批量插入（队列缓冲，最多 1000 条）

---

### 11.2 `alarm_log` 表（告警日志）

| 字段名           | 数据类型           | 是否可空 | 主键 | 说明                                  |
| ---------------- | ------------------ | -------- | ---- | ------------------------------------- |
| `id`             | NVARCHAR(100)      | ❌ NOT NULL | ✅   | 主键，格式 `alarm_{时间戳}`               |
| `device_id`      | NVARCHAR(50)       | ✅      |      | 触发告警的设备 ID                        |
| `alarm_type`     | NVARCHAR(50)       | ✅      |      | 告警类型：`temperature_high` / `temperature_low` / `humidity_high` / `humidity_low` |
| `alarm_message`  | NVARCHAR(255)      | ✅      |      | 告警消息，如 `温度过高: 36.5℃`            |
| `create_time`    | DATETIME           | ✅      |      | 告警触发时间，默认 `GETDATE()`            |

**数据示例**:

```
id                          | device_id      | alarm_type        | alarm_message        | create_time
----------------------------+----------------+-------------------+---------------------+-------------------
alarm_1718000000            | esp32_s3_abcd  | temperature_high  | 温度过高: 36.5℃       | 2024-06-10 14:30:00
alarm_1718000060            | esp32_s3_abcd  | humidity_low      | 湿度过低: 18.0%       | 2024-06-10 14:31:00
```

**触发条件**（后端阈值）:

| 指标   | 下限      | 上限      |
| ------ | --------- | --------- |
| 温度   | < 15°C    | > 35°C    |
| 湿度   | < 20%     | > 80%     |

---

### 11.3 `device_status` 表（设备在线状态）

| 字段名           | 数据类型           | 是否可空 | 主键 | 说明                           |
| ---------------- | ------------------ | -------- | ---- | ------------------------------ |
| `id`             | NVARCHAR(100)      | ❌ NOT NULL | ✅   | 主键，格式 `device_{device_id}`  |
| `device_id`      | NVARCHAR(50)       | ✅      |      | 设备 ID                        |
| `online_status`  | NVARCHAR(20)       | ✅      |      | 状态：`online` / `offline`      |
| `last_online`    | DATETIME           | ✅      |      | 最后一次心跳时间                  |

**数据示例**:

```
id                    | device_id      | online_status | last_online
----------------------+----------------+---------------+-------------------
device_esp32_s3_abcd  | esp32_s3_abcd  | online        | 2024-06-10 14:31:00
```

**更新方式**: ESP32 每 30 秒发送心跳到 `lab/device/heartbeat`，后端收到后更新此表

---

### 11.4 ORM 模型定义（[backend/database/db.py](file:///e:/graduationProject/SmartLab-AIoT/backend/database/db.py#L12-L38)）

```python
class SensorData(Base):
    __tablename__ = "sensor_data"
    id = Column(String(100), primary_key=True)
    device_id = Column(String(50))
    temperature = Column(Float)
    humidity = Column(Float)
    light = Column(Float)
    window_open = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.now)

class AlarmLog(Base):
    __tablename__ = "alarm_log"
    id = Column(String(100), primary_key=True)
    device_id = Column(String(50))
    alarm_type = Column(String(50))
    alarm_message = Column(String(255))
    create_time = Column(DateTime, default=datetime.now)

class DeviceStatus(Base):
    __tablename__ = "device_status"
    id = Column(String(100), primary_key=True)
    device_id = Column(String(50))
    online_status = Column(String(20))
    last_online = Column(DateTime)
```

### 10.4 前端告警阈值（[frontend/index.html](file:///e:/graduationProject/SmartLab-AIoT/frontend/index.html) `ALARM_CFG`）

```js
{
  temperature: { min: 15, max: 30 },
  humidity:    { min: 30, max: 60 },
  light:       { min: 800, max: 3200 }
}
```

***

**文档版本**: v1.0 · 2026年6月9日 · 基于 SQL Server + SQLAlchemy ORM 实现
