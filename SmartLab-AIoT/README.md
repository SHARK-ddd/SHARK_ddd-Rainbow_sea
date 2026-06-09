# SmartLab-AIoT 智慧机房环境监测系统

> 🎓 毕业设计项目 | 基于 ESP32-S3 + FastAPI + MQTT 的物联网环境监测平台

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136+-green.svg)](https://fastapi.tiangolo.com/)
[![ESP32](https://img.shields.io/badge/ESP32-S3--N16R8-orange.svg)](https://www.espressif.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📖 目录导航

- [项目简介](#-项目简介)
- [技术架构](#-技术架构)
- [功能特性](#-功能特性)
- [快速开始](#-快速开始)
- [项目结构](#-项目结构)
- [API 文档](#-api-文档)
- [常见问题](#-常见问题)
- [开发计划](#-开发计划)

---

## 🌟 项目简介

SmartLab-AIoT 是一个**完整的物联网环境监测系统**，实现了从硬件传感器到 Web 可视化的全栈解决方案。

### 核心功能

```
┌─────────────┐    MQTT     ┌─────────────┐   WebSocket  ┌─────────────┐
│  ESP32 设备  │ ─────────>  │  后端服务   │ ──────────>  │  Web 前端    │
│  传感器采集  │  消息队列   │  数据处理   │  实时推送    │  监控大屏   │
└─────────────┘             └─────────────┘              └─────────────┘
     ↓                           ↓                            ↓
  温湿度/光照                  SQLite 存储                  ECharts 图表
  门窗状态                    告警记录                      实时更新
```

### 应用场景

- ✅ **机房环境监测** - 实时监控温湿度、光照、门窗状态
- ✅ **智能告警** - 温度/湿度异常自动告警
- ✅ **数据可视化** - 实时图表展示历史趋势
- ✅ **设备管理** - 多设备接入与状态监控

---

## 🏗️ 技术架构

### 系统架构图

```
┌─────────────────────────────────────────────────────────────────────┐
│                         用户层 (User Layer)                         │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Web Dashboard (Bootstrap + ECharts)      │   │
│  │         实时监控 · 历史图表 · 告警列表 · 设备状态            │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                ↑ WebSocket (实时推送)
┌─────────────────────────────────────────────────────────────────────┐
│                      应用层 (Application Layer)                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                   FastAPI Backend Service                   │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │   │
│  │  │  MQTT    │  │ WebSocket│  │ REST API │  │  Database│   │   │
│  │  │  Listener│  │ Broadcaster│  │ Endpoints│  │  SQLite  │   │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                ↑ MQTT Protocol
┌─────────────────────────────────────────────────────────────────────┐
│                       通信层 (Communication Layer)                  │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Mosquitto MQTT Broker                    │   │
│  │              端口：1883 | 协议：MQTT 3.1.1                  │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                ↑ MQTT Protocol
┌─────────────────────────────────────────────────────────────────────┐
│                        设备层 (Device Layer)                        │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    ESP32-S3-N16R8 Controller                │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────────┐   │   │
│  │  │ DHT22   │  │ BH1750  │  │ 磁簧开关 │  │   WiFi      │   │   │
│  │  │温湿度   │  │ 光照    │  │ 门窗检测 │  │  网络通信   │   │   │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────────┘   │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

### 技术栈详情

| 层级 | 技术 | 版本 | 用途 |
|------|------|------|------|
| **硬件** | ESP32-S3-N16R8 | - | 主控芯片（16MB Flash, 8MB PSRAM） |
| **传感器** | DHT22 | - | 温湿度检测（精度：±0.5℃, ±2%RH） |
| **传感器** | BH1750 | - | 光照强度检测（1-65535 lux） |
| **传感器** | 磁簧开关 | - | 门窗状态检测（常开/常闭） |
| **通信** | MQTT | 3.1.1 | 设备与服务器消息传输 |
| **后端** | FastAPI | 0.136+ | 高性能 Web 框架 |
| **服务器** | Uvicorn | 最新 | ASGI 服务器 |
| **数据库** | SQLite | 内置 | 轻量级数据存储 |
| **ORM** | SQLAlchemy | 2.0+ | 数据库操作 |
| **前端** | Bootstrap 5 | 最新 | UI 响应式布局 |
| **图表** | ECharts | 5.0+ | 数据可视化 |
| **实时** | WebSocket | - | 毫秒级数据推送 |

---

## ✨ 功能特性

### ✅ 已实现功能

| 模块 | 功能 | 状态 | 说明 |
|------|------|------|------|
| **硬件层** | 传感器数据采集 | ✅ 完成 | DHT22 温湿度 + BH1750 光照 |
| | WiFi 自动连接 | ✅ 完成 | 断线自动重连 |
| | MQTT 消息发布 | ✅ 完成 | QoS 0 级别 |
| | 设备心跳上报 | ✅ 完成 | 30 秒/次 |
| **后端层** | MQTT 消息订阅 | ✅ 完成 | 多主题订阅 |
| | RESTful API | ✅ 完成 | 数据查询/提交 |
| | WebSocket 推送 | ✅ 完成 | 实时广播 |
| | SQLite 存储 | ✅ 完成 | 批量插入优化 |
| | 告警检测 | ✅ 完成 | 阈值自动判断 |
| **前端层** | 实时监控大屏 | ✅ 完成 | 数据动态刷新 |
| | 历史数据图表 | ✅ 完成 | ECharts 折线图 |
| | 告警信息展示 | ✅ 完成 | 列表展示 |
| | 设备状态监控 | ✅ 完成 | 在线/离线指示 |

### 🔄 开发中功能

- [ ] **用户认证系统** - JWT Token 认证
- [ ] **告警规则配置** - 自定义阈值设置
- [ ] **历史数据查询** - 时间范围筛选
- [ ] **数据导出功能** - CSV/Excel 导出

### 📋 规划功能

- [ ] **Docker 容器化** - 一键部署
- [ ] **多设备管理** - 设备分组与拓扑
- [ ] **移动端适配** - 响应式优化
- [ ] **微信推送告警** - 企业微信通知
- [ ] **AI 异常检测** - 机器学习预测

---

## 🚀 快速开始

### 前置要求

| 软件 | 版本 | 用途 | 下载地址 |
|------|------|------|----------|
| Python | 3.8+ | 后端运行 | [python.org](https://www.python.org/) |
| Mosquitto | 2.0+ | MQTT Broker | [mosquitto.org](https://mosquitto.org/) |
| Thonny IDE | 最新 | ESP32 烧录 | [thonny.org](https://thonny.org/) |

### 方式一：一键启动（推荐）

```bash
# Windows PowerShell
cd e:\graduationProject\SmartLab-AIoT
.\start_all.ps1
```

### 方式二：分步启动

#### 1. 启动 MQTT Broker

```bash
# Windows
cd hardware
start_mosquitto.bat

# Linux/Mac
mosquitto -c mosquitto.conf -d
```

#### 2. 安装后端依赖

```bash
cd backend
pip install -r requirements.txt
```

#### 3. 启动后端服务

```bash
python main.py
```

访问：
- 🌐 API 文档：http://localhost:8000/docs
- � 健康检查：http://localhost:8000/health

#### 4. 打开前端页面

直接双击打开 `frontend/index.html`

---

### ESP32 固件烧录

#### 步骤 1：准备 MicroPython 固件

```bash
# 下载 ESP32-S3 MicroPython 固件
# 地址：https://micropython.org/download/ESP32_GENERIC_S3/
```

#### 步骤 2：使用 Thonny IDE 烧录

1. 打开 Thonny IDE
2. 工具 → 选项 → MicroPython
3. 选择 ESP32-S3 固件文件
4. 点击"安装 MicroPython"

#### 步骤 3：上传代码

上传以下文件到 ESP32：
- `hardware/main.py` - 主程序
- `hardware/sensor.py` - 传感器驱动
- `hardware/mqtt.py` - MQTT 客户端
- `hardware/wifi.py` - WiFi 管理

#### 步骤 4：配置网络

编辑 `hardware/main.py`：

```python
WIFI_SSID = "你的 WiFi 名称"
WIFI_PASSWORD = "你的 WiFi 密码"
MQTT_SERVER = "你的电脑 IP 地址"  # 如：192.168.1.100
```

#### 步骤 5：运行程序

在 Thonny 中运行 `main.py`，观察控制台输出。

---

## �📁 项目结构

```
SmartLab-AIoT/
│
├── 📂 backend/                 # FastAPI 后端服务
│   ├── 📂 api/                 # API 路由层
│   │   ├── routes.py           # 路由定义（传感器数据接口）
│   │   └── __init__.py         # 包导出
│   ├── 📂 database/            # 数据库操作层
│   │   ├── db.py               # SQLite 操作（模型+CRUD）
│   │   └── __init__.py
│   ├── 📂 mqtt/                # MQTT 客户端（预留）
│   │   └── __init__.py
│   ├── 📂 utils/               # 工具模块
│   │   └── __init__.py
│   ├── 📂 tests/               # 测试用例
│   │   ├── test_api.py         # API 接口测试
│   │   └── __init__.py
│   ├── main.py                 # 应用入口（WebSocket+MQTT）
│   ├── requirements.txt        # Python 依赖包
│   └── start.bat               # 一键启动脚本
│
├── 📂 hardware/                # ESP32 硬件代码
│   ├── main.py                 # 主程序（设备控制）
│   ├── sensor.py               # 传感器驱动（DHT22/BH1750）
│   ├── mqtt.py                 # MQTT 发布客户端
│   ├── mqtt_subscribe.py       # MQTT 订阅调试工具
│   ├── wifi.py                 # WiFi 连接管理
│   └── start_mosquitto.bat     # MQTT Broker 启动脚本
│
├── 📂 frontend/                # Web 前端
│   ├── index.html              # 监控 Dashboard
│   ├── package.json            # 前端依赖配置
│   ├── public/                 # 静态资源
│   └── src/                    # 源码目录
│
├── 📂 data/                    # 运行时数据（Git 忽略）
│   └── smartlab.db             # SQLite 数据库文件
│
├── 📂 docs/                    # 项目文档
│   ├── TECHNICAL_DOCUMENTATION.md  # 技术文档
│   ├── project_status.md       # 项目状态报告
│   └── plans/                  # 开发计划归档
│
├── .gitignore                  # Git 忽略配置
├── start_all.ps1               # 一键启动脚本（总入口）
└── README.md                   # 项目说明文档
```

---

## 📡 API 文档

### 接口列表

#### 1. 健康检查

```http
GET /health
```

**响应示例：**
```json
{
  "status": "ok",
  "service": "smartlab-backend",
  "websocket_clients": 3
}
```

---

#### 2. 上传传感器数据

```http
POST /api/sensor/data
Content-Type: application/json

{
  "sensor_id": "esp32-001",
  "sensor_type": "temperature",
  "value": 25.5,
  "timestamp": "2026-06-09T10:30:00"
}
```

**响应示例：**
```json
{
  "status": "received",
  "data": {
    "sensor_id": "esp32-001",
    "sensor_type": "temperature",
    "value": 25.5,
    "timestamp": "2026-06-09T10:30:00"
  }
}
```

---

#### 3. 查询历史数据

```http
GET /api/sensor/data?sensor_id=esp32-001&limit=50
```

**查询参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| sensor_id | string | 否 | 设备 ID（不传则查询所有） |
| sensor_type | string | 否 | 传感器类型 |
| limit | int | 否 | 返回数量上限（1-1000，默认 100） |

**响应示例：**
```json
[
  {
    "sensor_id": "esp32-001",
    "sensor_type": "temperature",
    "value": 25.5,
    "timestamp": "2026-06-09T10:30:00"
  },
  {
    "sensor_id": "esp32-001",
    "sensor_type": "temperature",
    "value": 25.3,
    "timestamp": "2026-06-09T10:29:00"
  }
]
```

---

#### 4. WebSocket 实时推送

```
ws://localhost:8000/ws
```

**推送数据格式：**
```json
{
  "device_id": "esp32-001",
  "temperature": 25.5,
  "humidity": 60,
  "light": 500,
  "window_open": false,
  "timestamp": "2026-06-09T10:30:00"
}
```

---

### MQTT Topic 设计

| Topic | 方向 | 用途 | 消息格式 |
|-------|------|------|----------|
| `lab/device/data` | ESP32 → Server | 传感器数据上报 | JSON（温湿度/光照） |
| `lab/device/heartbeat` | ESP32 → Server | 设备心跳 | JSON（设备 ID + 时间戳） |
| `lab/device/alarm` | Server → ESP32 | 告警通知 | JSON（告警类型 + 消息） |

---

## ❓ 常见问题

### 1. MQTT Broker 启动失败

**问题：** `mosquitto.exe` 无法启动

**解决方案：**
```bash
# 检查端口是否被占用
netstat -ano | findstr :1883

# 杀掉占用进程或修改 Mosquitto 端口
```

---

### 2. ESP32 无法连接 WiFi

**问题：** 控制台显示 `WiFi connection failed`

**解决方案：**
- 检查 WiFi 名称和密码是否正确
- 确认 ESP32 与电脑在同一局域网
- 尝试重启路由器

---

### 3. 后端服务无法启动

**问题：** `ModuleNotFoundError: No module named 'fastapi'`

**解决方案：**
```bash
cd backend
pip install -r requirements.txt
```

---

### 4. 数据库文件不存在

**问题：** `data/smartlab.db` 找不到

**解决方案：**
- 首次运行后端会自动创建
- 检查 `data/` 文件夹是否有写入权限
- 手动创建空文件夹即可

---

### 5. WebSocket 连接失败

**问题：** 前端无法连接到 `ws://localhost:8000/ws`

**解决方案：**
- 确认后端服务已启动
- 检查防火墙是否阻止 8000 端口
- 浏览器控制台查看错误信息

---

## 📅 开发计划

### V1.0 ✅ 已完成（2026.05）

- ESP32 传感器数据采集
- MQTT 消息传输
- FastAPI 后端服务
- WebSocket 实时推送
- 基础 Dashboard 展示

### V1.1 🔄 开发中（2026.06）

- 用户认证系统（JWT）
- 告警规则配置页面
- 历史数据查询 API
- 数据导出功能（CSV）

### V1.2 📋 规划中（2026.07）

- Docker 容器化部署
- 多设备管理面板
- 移动端响应式优化
- 企业微信推送告警

### V2.0 🎯 远景（2026.08+）

- AI 异常检测（LSTM 预测）
- YOLO 人员识别
- OTA 远程固件升级
- 云服务器部署

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 开发规范

- 代码风格遵循 [PEP8](https://pep8.org/) (Python)
- 提交信息使用英文描述
- 新增功能需提供测试用例

### 提交步骤

1. Fork 本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 👨‍💻 关于项目

- **项目类型：** 毕业设计
- **开发时间：** 2026 年 3 月 - 2026 年 6 月
- **技术栈：** ESP32 + MicroPython + FastAPI + WebSocket
- **应用场景：** 智慧机房、智能楼宇、环境监测

---

## 📞 联系方式

如有问题或建议，请提交 Issue 或发送邮件至：

📧 Email: [your-email@example.com]

---

<div align="center">

**项目状态：** ✅ 活跃开发中  
**当前版本：** v1.0  
**最后更新：** 2026 年 6 月 9 日

⭐ 如果这个项目对你有帮助，请给一个 Star！

</div>
