"""
API 模块 - 统一导出路由配置

这个文件的作用：
- 作为 api 模块的入口文件
- 从 routes.py 导入 router 对象
- 让 main.py 可以通过 `from api import router` 简洁导入

文件结构：
api/
├── __init__.py    ← 这个文件（中转站）
└── routes.py      ← 实际的 API 路由定义
"""
from .routes import router
