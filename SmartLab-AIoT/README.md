# AIoT Smart Lab Monitoring System

> 基于 ESP32-S3 的智慧机房环境监测系统

---

## 一、项目简介

SmartLab-AIoT 是一个完整的物联网环境监测平台，实现了从传感器数据采集到Web实时可视化的完整闭环。

### 🌟 核心目标

- **环境数据实时采集** - ESP32传感器节点采集温湿度、光照等数据
- **MQTT云端通信** - 可靠的物联网消息传输
- **FastAPI后端处理** - 高性能数据处理服务
- **WebSocket实时推送** - 毫秒级数据更新到前端
- **Web可视化管理** - 现代化监控Dashboard

---

## 二、技术栈

### 🔧 硬件层
| 组件 | 技术 | 说明 |
|------|------|------|
| 主控芯片 | ESP32-S3-N16R8 | 16MB Flash, 8MB PSRAM |
| 传感器 | DHT22 | 温湿度采集 |
| 传感器 | BH1750 | 光照强度检测 |
| 传感器 | 磁簧开关 | 门窗状态检测 |

### 🖥️ 后端层
| 组件 | 技术 | 版本 |
|------|------|------|
| 框架 | FastAPI | 0.136.3 |
| 服务器 | Uvicorn | 最新 |
| MQTT客户端 | paho-mqtt | 最新 |
| 数据库 | SQLite | 内置 |
| ORM | SQLAlchemy | 最新 |

### 🌐 前端层
| 组件 | 技术 | 说明 |
|------|------|------|
| UI框架 | Bootstrap 5 | 响应式布局 |
| 图表库 | ECharts | 数据可视化 |
| 图标 | Font Awesome | 图标库 |
| 实时通信 | WebSocket | 实时推送 |

---

## 三、功能特性

### ✅ 已实现功能
- [x] ESP32传感器数据采集
- [x] WiFi自动连接与重连
- [x] MQTT消息发布
- [x] FastAPI后端服务
- [x] MQTT订阅服务
- [x] SQLite数据持久化
- [x] WebSocket实时推送
- [x] 实时监控Dashboard
- [x] 温湿度/光照折线图

### 🔄 开发中功能
- [ ] 用户认证系统
- [ ] 告警通知机制
- [ ] 历史数据查询API
- [ ] 数据导出功能

### 📋 规划功能
- [ ] Docker容器化部署
- [ ] 多设备管理
- [ ] 移动端适配
- [ ] 微信推送告警

---

## 四、项目架构

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

### 📁 目录结构

```
SmartLab-AIoT/
├── backend/                 # FastAPI 后端服务
│   ├── api/                 # API 路由层
│   │   ├── routes.py        # 路由定义
│   │   └── __init__.py      # 包导出
│   ├── database/            # 数据库操作层
│   │   ├── db.py            # SQLite 操作
│   │   └── __init__.py
│   ├── mqtt/                # MQTT 客户端(预留)
│   │   └── __init__.py
│   ├── utils/               # 工具模块
│   │   ├── influxdb_utils.py # InfluxDB 工具
│   │   └── __init__.py
│   ├── tests/               # 测试用例
│   │   ├── test_api.py      # API 测试脚本
│   │   └── __init__.py
│   ├── main.py              # 应用入口
│   ├── requirements.txt     # Python 依赖
│   └── start.bat            # 一键启动脚本
├── hardware/                # ESP32 硬件层
│   ├── main.py              # 主程序
│   ├── sensor.py            # 传感器驱动(DHT22/BH1750/磁簧)
│   ├── mqtt.py              # MQTT 发布客户端
│   ├── mqtt_subscribe.py    # MQTT 订阅调试
│   ├── mqtt_test.py         # MQTT 功能测试
│   ├── wifi.py              # WiFi 连接管理
│   ├── query                # 查询脚本
│   └── start_mosquitto.bat  # MQTT Broker 启动脚本
├── frontend/                # Web 前端
│   ├── index.html           # 监控 Dashboard
│   ├── package.json         # 前端依赖配置
│   ├── public/              # 静态资源
│   ├── src/                 # 源码目录
│   │   ├── components/      # 组件
│   │   └── views/           # 视图
│   └── components/          # 页面组件
├── docs/                    # 项目文档
│   ├── project_status.md    # 项目状态报告
│   ├── visualization_plan.md # 可视化方案
│   └── plans/               # 开发计划归档
├── data/                    # 运行时数据(gitignored)
│   └── smartlab.db          # SQLite 数据库
└── README.md                # 项目说明
```

---

## 五、快速开始

### 📦 环境要求

- Python 3.8+
- Mosquitto MQTT Broker
- ESP32 MicroPython 固件

### 🚀 启动步骤

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

### 📱 ESP32 部署

1. 使用 Thonny 烧录 MicroPython 固件
2. 上传以下文件到 ESP32：
   - `main.py` - 主程序
   - `sensor.py` - 传感器驱动
   - `mqtt.py` - MQTT客户端
   - `wifi.py` - WiFi连接
3. 修改 `wifi.py` 中的 WiFi 配置
4. 运行 `main.py`

---

## 六、版本路线

### 🎯 V1.0 (已完成)
- ESP32传感器数据采集
- MQTT消息传输
- FastAPI后端服务
- WebSocket实时推送
- 基础Dashboard展示

### 🎯 V1.1 (开发中)
- 用户认证系统
- 告警规则配置
- 历史数据查询
- 数据导出功能

### 🎯 V1.2 (规划中)
- Docker容器化部署
- 多设备管理面板
- 移动端响应式优化
- 微信推送告警

### 🎯 V2.0 (远景)
- AI异常检测
- YOLO人员识别
- OTA远程升级
- 云服务器部署

---

## 七、API 接口

### 健康检查
```
GET /health
```

### 传感器数据
```
GET  /api/sensor/data          # 查询历史数据
POST /api/sensor/data          # 提交传感器数据
```

### WebSocket
```
ws://localhost:8000/ws         # 实时数据推送
```

---

## 八、MQTT Topic 设计

| Topic | 用途 | 说明 |
|-------|------|------|
| `lab/device/data` | 传感器数据 | 温度、湿度、光照 |
| `lab/device/heartbeat` | 设备心跳 | 在线状态检测 |
| `lab/device/alarm` | 告警消息 | 异常告警通知 |

---

## 九、贡献指南

欢迎提交 Issue 和 Pull Request！

### 开发规范
- 代码风格遵循 PEP8 (Python)
- 提交信息使用英文描述
- 新增功能需提供测试用例

---

## 十、许可证

MIT License

---

**项目状态**: ✅ 活跃开发中  
**最后更新**: 2026年6月  
**版本**: v1.0