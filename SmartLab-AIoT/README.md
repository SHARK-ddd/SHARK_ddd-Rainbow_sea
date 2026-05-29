# SmartLab-AIoT

## 项目简介

SmartLab-AIoT 是一个智能实验室物联网系统，旨在通过物联网技术实现实验室环境的智能化监控与管理。

## 技术栈

- **后端**: FastAPI + Python
- **前端**: Vue.js + Element Plus
- **硬件**: ESP32
- **AI**: YOLO (目标检测)
- **通信**: MQTT / WebSocket
- **数据库**: SQLite / MySQL

## 功能特性

- 环境监测（温湿度、光照等）
- 设备状态监控
- 实时数据展示
- 智能控制

## 项目架构

```
SmartLab-AIoT/
├── docs/          # 文档
├── hardware/      # 硬件代码
├── backend/       # 后端服务
├── frontend/      # 前端界面
├── ai/            # AI模型
├── deploy/        # 部署脚本
├── data/          # 数据存储
└── demo/          # 演示素材
```

## 快速开始

### 后端启动

```bash
cd backend
pip install -r requirements.txt
python main.py
```

### 前端启动

```bash
cd frontend
npm install
npm run dev
```

## 版本路线

- **V1**: ESP32数据采集 + FastAPI后端 + 基础网页显示
- **V2**: YOLO人数检测功能
- **V3**: 自动控制 + WebSocket实时通信
- **V4**: 云部署 + MQTT + 多机房管理

## 目录结构

详细目录说明请参考项目结构文档。

## 贡献

欢迎提交Issue和Pull Request。

## 许可证

MIT License