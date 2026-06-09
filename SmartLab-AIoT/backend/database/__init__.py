"""
Database 模块 - 数据库操作封装

这个文件的作用：
- 作为 database 模块的入口文件（目前为空）
- 标记 database 文件夹为 Python 包
- 后续可以在这里统一导出数据库操作函数

文件结构：
database/
├── __init__.py    ← 这个文件（模块入口）
└── db.py          ← 实际的数据库操作（模型定义 + CRUD 函数）

使用方式：
from database.db import save_sensor_data, get_sensor_data
"""