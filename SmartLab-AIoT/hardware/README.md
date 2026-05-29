# ESP32 硬件使用说明

## 准备工作

### 1. 烧录 MicroPython 固件

1. 访问 https://micropython.org/download/ESP32_GENERIC/
2. 下载最新版 `.bin` 文件
3. 用 Thonny 烧录：
   - 工具 → 配置解释器 → 选择 MicroPython (ESP32)
   - 点击 "安装或更新 MicroPython"
   - 选择下载的 `.bin` 文件并安装

### 2. 硬件连接

```
ESP32 Pin    光敏模块
VCC    →     3.3V
GND    →     GND
AO     →     GPIO34
```

## 代码配置

修改 `hardware/main.py` 中的配置：

```python
WIFI_SSID = "你的WiFi名称"
WIFI_PASSWORD = "你的WiFi密码"
BACKEND_URL = "http://你的电脑IP:8000/api/sensor/data"
```

## 获取电脑IP

Windows 运行：
```bash
ipconfig
```
找到 "IPv4 地址"，例如 `192.168.1.100`

## 运行

在 Thonny 中打开 `main.py`，点击运行按钮即可。

## 预期输出

```
正在连接 WiFi: 你的WiFi名称...
.....
WiFi 连接成功!
IP 地址: 192.168.1.101

开始采集光敏数据...
光敏值: 2456
发送成功: {"status":"received",...}
光敏值: 2034
...
```