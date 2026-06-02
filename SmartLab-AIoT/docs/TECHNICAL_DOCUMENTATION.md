# SmartLab-AIoT 技术架构文档

---

## 一、项目概述

### 1.1 项目定位
**SmartLab-AIoT** 是一个基于 ESP32-S3 的智慧实验室环境监测系统，实现从传感器数据采集到 Web 实时可视化的完整闭环。

### 1.2 核心目标
| 目标 | 描述 |
|------|------|
| 环境数据实时采集 | ESP32传感器节点采集温湿度、光照、门窗状态 |
| MQTT云端通信 | 可靠的物联网消息传输协议 |
| FastAPI后端处理 | 高性能数据处理服务 |
| WebSocket实时推送 | 毫秒级数据更新到前端 |
| Web可视化管理 | 现代化监控Dashboard |

### 1.3 项目状态
- **当前版本**: v1.0
- **项目状态**: ✅ 活跃开发中
- **最后更新**: 2026年6月

---

## 二、技术栈

### 2.1 硬件层

| 组件 | 技术 | 说明 |
|------|------|------|
| 主控芯片 | ESP32-S3-N16R8 | 16MB Flash, 8MB PSRAM |
| 温湿度传感器 | DHT22/DHT11 | 温湿度采集 |
| 光照传感器 | BH1750/光敏电阻 | 光照强度检测 |
| 门窗传感器 | 磁簧开关 | 门窗状态检测 |
| 通信模块 | WiFi 802.11b/g/n | 网络通信 |

### 2.2 后端层

| 组件 | 技术 | 版本 |
|------|------|------|
| 框架 | FastAPI | 0.136.3 |
| 服务器 | Uvicorn | 最新 |
| MQTT客户端 | paho-mqtt | 最新 |
| 数据库 | SQLite | 内置 |
| InfluxDB | influxdb-client | 规划中 |
| ORM | SQLAlchemy | 最新 |
| 配置 | python-dotenv | 最新 |
| 数据验证 | Pydantic | 最新 |

### 2.3 前端层

| 组件 | 技术 | 说明 |
|------|------|------|
| UI框架 | Bootstrap 5 | 响应式布局 |
| 图表库 | ECharts | 数据可视化 |
| 图标 | Font Awesome | 图标库 |
| 实时通信 | WebSocket | 实时推送 |
| 动画效果 | CSS3 Animations | 交互动效 |

---

## 三、系统架构

### 3.1 架构分层图

```
┌─────────────────────────────────────────────────────────────────┐
│                       Web 前端层                               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Dashboard 实时监控 · 历史图表 · 告警展示 · 设备状态    │   │
│  │         WebSocket ←─── 实时数据推送                      │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↑ WebSocket
┌─────────────────────────────────────────────────────────────────┐
│                       FastAPI 后端层                           │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   │
│  │ MQTT     │   │ WebSocket│   │ REST API │   │ Database │   │
│  │ 订阅服务 │ → │ 广播服务 │   │ 数据接口 │   │ SQLite   │   │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↑ MQTT
┌─────────────────────────────────────────────────────────────────┐
│                        MQTT Broker                            │
│                    Mosquitto (端口: 1883)                      │
└─────────────────────────────────────────────────────────────────┘
                              ↑ MQTT
┌─────────────────────────────────────────────────────────────────┐
│                      ESP32 硬件层                              │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   │
│  │  DHT22   │   │ BH1750   │   │ 磁簧开关 │   │  WiFi    │   │
│  │ 温湿度   │   │ 光照     │   │ 门窗检测 │   │ 网络通信 │   │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 端到端数据流

```
ESP32传感器采集 → MQTT发布(lab/device/data) → Mosquitto Broker → FastAPI订阅 → SQLite存储 → WebSocket广播 → 前端Dashboard展示
```

---

## 四、项目目录结构

```
SmartLab-AIoT/
├── backend/                 # FastAPI 后端服务
│   ├── api/                 # API 路由层
│   │   ├── routes.py        # 路由定义 (✅ 已实现)
│   │   └── __init__.py      # 包导出
│   ├── database/            # 数据库操作层
│   │   ├── db.py            # SQLite 操作 (✅ 已实现)
│   │   └── __init__.py
│   ├── mqtt/                # MQTT 客户端(预留)
│   │   └── __init__.py
│   ├── utils/               # 工具模块
│   │   ├── influxdb_utils.py # InfluxDB 工具 (✅ 已实现)
│   │   └── __init__.py
│   ├── tests/               # 测试用例
│   │   ├── test_api.py      # API 测试脚本
│   │   └── __init__.py
│   ├── main.py              # 应用入口 (✅ 已实现)
│   ├── requirements.txt     # Python 依赖
│   └── .env.example         # 环境变量示例
├── hardware/                # ESP32 硬件层
│   ├── main.py              # 主程序 (✅ 已实现)
│   ├── sensor.py            # 传感器驱动 (✅ 已实现)
│   ├── mqtt.py              # MQTT 发布客户端 (✅ 已实现)
│   ├── mqtt_subscribe.py    # MQTT 订阅调试
│   ├── mqtt_test.py         # MQTT 功能测试
│   ├── wifi.py              # WiFi 连接管理 (✅ 已实现)
│   ├── query/               # 查询脚本
│   ├── start_mosquitto.bat  # MQTT Broker 启动脚本
│   ├── PROJECT_SUMMARY.md   # 硬件项目总结
│   └── TROUBLESHOOTING_GUIDE.md # 故障排除指南
├── frontend/                # Web 前端
│   ├── index.html           # 监控 Dashboard (✅ 已实现)
│   └── package.json         # 前端依赖配置
├── docs/                    # 项目文档
│   ├── plans/               # 开发计划归档
│   │   └── 2026-05-30-dark-tech-monitoring-panel.md
│   ├── project_status.md    # 项目状态报告
│   ├── visualization_plan.md # 可视化方案
│   └── TECHNICAL_DOCUMENTATION.md # 技术架构文档
├── data/                    # 运行时数据(gitignored)
│   └── smartlab.db          # SQLite 数据库
├── README.md                # 项目说明
└── start_all.ps1            # 一键启动脚本
```

---

## 五、核心模块实现

### 5.1 后端主程序 (main.py)

**功能职责**:
- FastAPI 应用初始化
- CORS 跨域配置
- WebSocket 连接管理
- MQTT 订阅服务
- 数据广播机制

**关键实现**:
- `ConnectionManager`: WebSocket 连接管理类，支持多客户端连接和消息广播
- MQTT 订阅线程: 独立线程监听 MQTT 消息，收到数据后广播到所有 WebSocket 客户端
- 数据存储: MQTT 消息同时写入 SQLite 数据库

**文件位置**: [backend/main.py](file:///e:/graduationProject/SmartLab-AIoT/backend/main.py)

### 5.2 API 路由层 (api/routes.py)

**已实现接口**:

| API路径 | 方法 | 功能 | 状态 |
|---------|------|------|------|
| `/health` | GET | 健康检查 | ✅ |
| `/api/sensor/data` | POST | 接收传感器数据 | ✅ |
| `/api/sensor/data` | GET | 查询传感器历史 | ✅ |
| `/api/influxdb/environment` | POST | 写入环境数据 | ✅ |
| `/api/influxdb/write` | POST | 写入通用数据 | ✅ |
| `/api/influxdb/query` | GET | 查询数据 | ✅ |
| `/api/influxdb/environment` | GET | 查询环境数据 | ✅ |
| `/api/influxdb/health` | GET | InfluxDB连接状态 | ✅ |

**文件位置**: [backend/api/routes.py](file:///e:/graduationProject/SmartLab-AIoT/backend/api/routes.py)

### 5.3 数据库层 (database/db.py)

**数据表结构**:

| 字段 | 类型 | 说明 |
|------|------|------|
| id | String | 主键 (sensor_id_timestamp) |
| sensor_id | String | 设备ID |
| sensor_type | String | 传感器类型 |
| value | Float | 传感器数值 |
| timestamp | DateTime | 时间戳 |

**数据库路径**: `data/smartlab.db`（自动创建）

**文件位置**: [backend/database/db.py](file:///e:/graduationProject/SmartLab-AIoT/backend/database/db.py)

### 5.4 ESP32 主程序 (hardware/main.py)

**核心功能**:
- WiFi 自动连接与重连
- MQTT 客户端连接
- 传感器数据采集（每5秒）
- 心跳消息发送（每30秒）
- 连接状态监控与自动重连

**文件位置**: [hardware/main.py](file:///e:/graduationProject/SmartLab-AIoT/hardware/main.py)

### 5.5 传感器驱动 (hardware/sensor.py)

**支持传感器**:
- **光敏传感器**: ADC 模拟信号读取 (GPIO3)
- **DHT11温湿度传感器**: 数字信号读取 (GPIO4)

**文件位置**: [hardware/sensor.py](file:///e:/graduationProject/SmartLab-AIoT/hardware/sensor.py)

### 5.6 MQTT客户端 (hardware/mqtt.py)

**功能特性**:
- 支持 MQTT 3.1.1 协议
- 连接状态管理
- 消息发布功能
- 断线自动重连

**文件位置**: [hardware/mqtt.py](file:///e:/graduationProject/SmartLab-AIoT/hardware/mqtt.py)

### 5.7 前端 Dashboard (frontend/index.html)

**可视化组件**:
| 组件 | 类型 | 说明 |
|------|------|------|
| 温度卡片 | 数值展示 | 实时温度显示 |
| 湿度卡片 | 数值展示 | 实时湿度显示 |
| 光照卡片 | 数值展示 | 实时光照强度 |
| 门窗状态 | 状态指示 | 开/关状态 |
| 告警面板 | 列表 | 异常告警信息 |
| 光照仪表盘 | ECharts Gauge | 光照强度仪表 |
| 湿度液态图 | ECharts LiquidFill | 湿度可视化 |
| 指标环形图 | ECharts Pie | 环境指标概览 |
| 温湿度堆叠图 | ECharts Bar | 对比分析 |
| 24小时热力图 | ECharts Heatmap | 历史趋势 |
| 温度趋势图 | ECharts Line | 温度变化曲线 |
| 光照趋势图 | ECharts Line | 光照变化曲线 |

**告警规则**:
- 温度: 低于15°C或高于30°C触发告警
- 湿度: 低于30%或高于60%触发告警
- 光照: 低于800lux或高于3200lux触发告警

**文件位置**: [frontend/index.html](file:///e:/graduationProject/SmartLab-AIoT/frontend/index.html)

---

## 六、MQTT Topic 设计

| Topic | 用途 | 消息格式 |
|-------|------|----------|
| `lab/device/data` | 传感器数据 | `{"device_id": "...", "temperature": 25.5, "humidity": 50, "light": 1200, "timestamp": 1620000000}` |
| `lab/device/heartbeat` | 设备心跳 | `{"device_id": "...", "status": "online"}` |
| `lab/device/alarm` | 告警消息 | 预留 |

---

## 七、已完成功能清单

### 7.1 后端功能

| 功能 | 状态 | 说明 |
|------|------|------|
| FastAPI 服务框架 | ✅ | 已实现 |
| MQTT 订阅服务 | ✅ | 实时接收传感器数据 |
| WebSocket 服务 | ✅ | 实时推送数据到前端 |
| SQLite 数据库 | ✅ | 数据持久化存储 |
| REST API 接口 | ✅ | 数据查询与写入 |
| InfluxDB 工具类 | ✅ | 预留时序数据库支持 |
| 健康检查接口 | ✅ | 服务状态监控 |

### 7.2 硬件功能

| 功能 | 状态 | 说明 |
|------|------|------|
| WiFi 连接管理 | ✅ | 自动连接与重连 |
| MQTT 客户端 | ✅ | 消息发布功能 |
| 光敏传感器采集 | ✅ | ADC 读取 |
| DHT11 温湿度采集 | ✅ | 数字传感器读取 |
| 定时数据上报 | ✅ | 每5秒一次 |
| 心跳检测 | ✅ | 每30秒发送 |
| 异常重连机制 | ✅ | 自动恢复连接 |

### 7.3 前端功能

| 功能 | 状态 | 说明 |
|------|------|------|
| 实时数据展示 | ✅ | 温湿度/光照/门窗状态 |
| WebSocket 连接 | ✅ | 实时数据推送 |
| ECharts 图表 | ✅ | 多种可视化组件 |
| 告警系统 | ✅ | 异常检测与展示 |
| 深色主题 | ✅ | 现代化UI设计 |
| 响应式布局 | ✅ | 移动端适配 |

---

## 八、待实现功能

### 8.1 高优先级

| 功能 | 描述 |
|------|------|
| 用户认证系统 | 用户登录、权限管理 |
| 历史数据查询 | 支持时间范围筛选 |
| 数据导出功能 | CSV/Excel 导出 |
| 告警通知机制 | 微信推送/邮件告警 |

### 8.2 中优先级

| 功能 | 描述 |
|------|------|
| 多设备管理 | 支持多个ESP32设备 |
| Docker 容器化 | 一键部署 |
| Nginx 反向代理 | 生产环境配置 |

### 8.3 低优先级

| 功能 | 描述 |
|------|------|
| OTA 远程升级 | ESP32固件远程更新 |
| AI 异常检测 | 智能数据分析 |
| YOLO 人员识别 | 视频监控集成 |

---

## 九、快速启动指南

### 9.1 环境要求

- Python 3.8+
- Mosquitto MQTT Broker
- ESP32 MicroPython 固件

### 9.2 启动步骤

```bash
# 1. 启动 MQTT Broker
cd SmartLab-AIoT/hardware
start_mosquitto.bat

# 2. 安装后端依赖
cd ../backend
pip install -r requirements.txt

# 3. 启动后端服务
python main.py
# 服务地址: http://localhost:8000
# 文档地址: http://localhost:8000/docs

# 4. 打开前端页面
# 直接在浏览器中打开 frontend/index.html
```

### 9.3 ESP32 部署

1. 使用 Thonny 烧录 MicroPython 固件
2. 上传以下文件到 ESP32：
   - `main.py` - 主程序
   - `sensor.py` - 传感器驱动
   - `mqtt.py` - MQTT客户端
   - `wifi.py` - WiFi连接
3. 修改 `wifi.py` 中的 WiFi 配置（SSID 和密码）
4. 运行 `main.py`

---

## 十、技术亮点

### 10.1 实时数据推送
- WebSocket 实现毫秒级数据更新
- 支持多客户端同时连接
- 断线自动重连机制

### 10.2 分布式架构
- MQTT 解耦设备端与服务端
- 支持水平扩展
- 松耦合设计

### 10.3 现代化可视化
- 丰富的图表组件
- 深色科技风 UI
- 响应式设计适配多端

### 10.4 健壮性设计
- 连接状态监控
- 自动重连机制
- 异常捕获与处理

---

## 十一、版本路线

| 版本 | 状态 | 功能 |
|------|------|------|
| V1.0 | ✅ 已完成 | ESP32传感器采集、MQTT传输、FastAPI后端、WebSocket推送、基础Dashboard |
| V1.1 | 🔄 开发中 | 用户认证、告警规则、历史数据查询、数据导出 |
| V1.2 | 📋 规划中 | Docker容器化、多设备管理、移动端优化、微信推送 |
| V2.0 | 📋 远景 | AI异常检测、YOLO人员识别、OTA升级、云服务器部署 |

---

## 十二、关键配置

### 12.1 WiFi 配置 (hardware/main.py)

```python
WIFI_SSID = "your_wifi_ssid"
WIFI_PASSWORD = "your_wifi_password"
MQTT_SERVER = "192.168.1.100"  # 服务器IP地址
MQTT_PORT = 1883
```

### 12.2 Mosquitto 配置

```ini
listener 1883          # 监听所有接口的 1883 端口
allow_anonymous true   # 允许匿名连接（开发环境）
```

### 12.3 Windows 防火墙规则

```powershell
New-NetFirewallRule -Name "Mosquitto_MQTT" `
    -Direction Inbound -Protocol TCP `
    -LocalPort 1883 -Action Allow
```

---

**文档版本**: v1.0  
**生成日期**: 2026年6月1日  
**适用对象**: 项目维护者、新开发者、技术评审人员