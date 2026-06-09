"""
Tests 模块 - 自动化测试

这个文件的作用：
- 作为 tests 模块的入口文件
- 标记 tests 文件夹为 Python 包
- 存放所有测试脚本

测试文件：
- test_api.py - API 接口测试（模拟设备发送数据）

运行测试：
直接运行测试脚本即可：
    python tests/test_api.py

测试内容：
- 模拟 ESP32 设备发送传感器数据
- 验证 API 接口是否正常接收
- 查询历史数据验证存储功能
"""