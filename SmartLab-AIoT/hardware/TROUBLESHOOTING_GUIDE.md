# ESP32 IoT 项目故障排查指南

---

## 📋 文档信息

| 项目 | 内容 |
|------|------|
| **文档名称** | ESP32 IoT 项目故障排查指南 |
| **适用范围** | ESP32-S3 MicroPython 开发 |
| **创建日期** | 2026年5月29日 |
| **版本** | v1.0 |

---

## 一、常见问题分类

### 1.1 硬件连接问题

| 问题类型 | 错误表现 | 排查优先级 |
|----------|----------|------------|
| 引脚错误 | `ValueError: invalid pin` | 高 |
| 电源问题 | 传感器无响应 | 高 |
| 接线错误 | 数据异常或无数据 | 高 |

### 1.2 网络通信问题

| 问题类型 | 错误表现 | 排查优先级 |
|----------|----------|------------|
| WiFi 连接失败 | 无法连接网络 | 高 |
| MQTT 连接失败 | `ECONNABORTED (113)` | 高 |
| 端口未开放 | 连接被拒绝 | 中 |

### 1.3 代码逻辑问题

| 问题类型 | 错误表现 | 排查优先级 |
|----------|----------|------------|
| 库版本不兼容 | `ModuleNotFoundError` | 中 |
| API 使用错误 | 属性不存在错误 | 中 |
| 时序问题 | 传感器读取失败 | 低 |

---

## 二、问题排查流程

### 2.1 网络连接问题排查

```
MQTT连接失败
    ↓
┌─────────────────────────────────────┐
│ 1. 检查 WiFi 连接                  │
│    → 确认 IP 地址获取成功          │
│    → 确认设备与服务器同网段        │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. 检查端口监听                    │
│    → netstat -ano | findstr :1883 │
│    → 确认 0.0.0.0:1883 正在监听   │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. 检查防火墙规则                  │
│    → 确认入站规则允许 1883 端口    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 4. 检查 Mosquitto 配置            │
│    → listener 1883                │
│    → allow_anonymous true         │
└─────────────────────────────────────┘
```

### 2.2 传感器问题排查

```
传感器数据异常
    ↓
┌─────────────────────────────────────┐
│ 1. 检查硬件接线                    │
│    → VCC → 3.3V (不是5V!)         │
│    → GND → GND                    │
│    → DATA → 指定引脚              │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. 测试传感器驱动                  │
│    → 运行最小测试代码              │
│    → 确认硬件正常                  │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. 检查代码逻辑                    │
│    → 确认引脚配置正确              │
│    → 确认时序符合传感器要求        │
└─────────────────────────────────────┘
```

---

## 三、问题解决方案库

### 3.1 引脚错误

**问题**：`ValueError: invalid pin`

**原因**：
- 使用了受限的 GPIO（如 RTC GPIO：GPIO34-GPIO39）
- MicroPython 固件不支持该引脚

**解决方案**：
```python
# 错误：使用受限引脚
self.sensor = ADC(machine.Pin(35))  # GPIO35 可能受限

# 正确：使用 ADC1 通道引脚
self.sensor = ADC(machine.Pin(3))   # GPIO3 兼容性好
```

**推荐引脚**：GPIO1-GPIO11（ADC1 通道）

---

### 3.2 MQTT 连接失败

**问题**：`OSError: [Errno 113] ECONNABORTED`

**原因**：
- Windows 防火墙阻止入站连接
- Mosquitto 未配置监听所有接口

**解决方案**：

1. **配置 Mosquitto**（`mosquitto.conf`）：
```ini
listener 1883
allow_anonymous true
```

2. **添加防火墙规则**：
```powershell
New-NetFirewallRule -Name "Mosquitto_MQTT" `
    -Direction Inbound -Protocol TCP `
    -LocalPort 1883 -Action Allow
```

---

### 3.3 DHT11 读取失败

**问题**：`'Pin' object has no attribute 'pin'` 或返回 `None`

**原因**：
- 自定义 DHT11 驱动时序问题
- MicroPython `Pin` 对象 API 使用错误

**解决方案**：
```python
# 使用 MicroPython 内置 DHT 驱动
from dht import DHT11
from machine import Pin

dht = DHT11(Pin(4))
dht.measure()
temperature = dht.temperature()
humidity = dht.humidity()
```

**接线要求**：
| DHT11 | ESP32 |
|-------|-------|
| VCC | 3.3V（必须！） |
| GND | GND |
| DO | GPIO4 |

---

### 3.4 光敏传感器数据异常

**问题**：光照值始终为 0 或 100

**原因**：
- 引脚配置错误
- ADC 衰减配置不正确

**解决方案**：
```python
# 正确配置 ADC
from machine import Pin, ADC

light_sensor = ADC(Pin(3))
light_sensor.atten(ADC.ATTN_11DB)  # 设置 11dB 衰减

raw_value = light_sensor.read()
light_percent = (raw_value / 4095) * 100
```

**衰减配置说明**：
| 衰减 | 电压范围 | 适用场景 |
|------|----------|----------|
| ATTN_0DB | 0-1.1V | 小信号 |
| ATTN_2_5DB | 0-1.5V | 一般信号 |
| ATTN_6DB | 0-2.2V | 较大信号 |
| ATTN_11DB | 0-3.3V | 全量程 |

---

### 3.5 库安装问题

**问题**：`ModuleNotFoundError: No module named 'paho'`

**原因**：
- Python 环境不一致
- 未安装所需库

**解决方案**：
```bash
# 确认 Python 路径
which python

# 使用正确的 Python 安装库
C:\Python314\python.exe -m pip install paho-mqtt
```

---

## 四、代码最佳实践

### 4.1 传感器驱动封装

```python
class SensorManager:
    def __init__(self):
        # 初始化传感器
        self.light_sensor = ADC(Pin(3))
        self.light_sensor.atten(ADC.ATTN_11DB)
        
        # 驱动可用性检测
        try:
            from dht import DHT11
            self.dht11 = DHT11(Pin(4))
            self.dht_available = True
        except ImportError:
            self.dht_available = False

    def read_light(self):
        try:
            value = self.light_sensor.read()
            return (value / 4095) * 100
        except Exception as e:
            print(f"读取失败: {e}")
            return None

    def read_dht11(self):
        if not self.dht_available:
            return None
        try:
            self.dht11.measure()
            return {
                "temperature": self.dht11.temperature(),
                "humidity": self.dht11.humidity()
            }
        except Exception as e:
            print(f"DHT11读取失败: {e}")
            return None
```

### 4.2 MQTT 客户端封装

```python
class MQTTManager:
    def __init__(self, client_id, server, port=1883):
        self.client = MQTTClient(client_id, server, port)
        self.connected = False

    def connect(self):
        try:
            self.client.connect()
            self.connected = True
            return True
        except OSError as e:
            print(f"MQTT连接失败: {e}")
            return False

    def publish(self, topic, payload):
        if not self.connected:
            return False
        try:
            self.client.publish(topic, payload)
            return True
        except Exception as e:
            print(f"发布失败: {e}")
            return False
```

### 4.3 异常处理模式

```python
def safe_operation(operation, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = operation()
            if result is not None:
                return result
        except Exception as e:
            print(f"尝试 {attempt+1} 失败: {e}")
        time.sleep(1)
    return None
```

---

## 五、快速检查清单

### 5.1 启动前检查

| 检查项 | 检查方法 | 预期结果 |
|--------|----------|----------|
| WiFi 配置 | 检查 SSID 和密码 | 正确配置 |
| MQTT 服务器 | `ping <server_ip>` | 响应正常 |
| 端口监听 | `netstat -ano | findstr :1883` | 显示 LISTENING |
| 防火墙规则 | Windows 防火墙设置 | 允许 1883 端口 |
| 传感器接线 | 目视检查 | VCC→3.3V, GND→GND |

### 5.2 运行时检查

| 检查项 | 检查方法 | 正常输出 |
|--------|----------|----------|
| WiFi 连接 | `wlan.isconnected()` | True |
| IP 地址 | `wlan.ifconfig()[0]` | 192.168.x.x |
| MQTT 连接 | `mqtt_manager.connected` | True |
| 传感器数据 | `sensor_manager.get_sensor_data()` | 包含有效数据 |

---

## 六、调试技巧

### 6.1 日志输出

```python
def debug_log(message, level="INFO"):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")

# 使用示例
debug_log("WiFi连接成功", "INFO")
debug_log(f"传感器值: {value}", "DEBUG")
```

### 6.2 分段测试

```python
# 测试 WiFi
wifi_manager = WiFiManager(SSID, PASSWORD)
ip = wifi_manager.connect()
print(f"IP: {ip}")

# 测试 MQTT
mqtt_manager = MQTTManager(DEVICE_ID, SERVER)
mqtt_manager.connect()

# 测试传感器
sensor_manager = SensorManager()
data = sensor_manager.get_sensor_data()
print(f"传感器数据: {data}")
```

---

## 七、常见错误码速查

| 错误码 | 含义 | 解决方案 |
|--------|------|----------|
| 113 | ECONNABORTED | 检查防火墙和端口 |
| 110 | ETIMEDOUT | 检查网络连接 |
| 2 | ENOENT | 文件不存在 |
| ValueError | invalid pin | 使用有效引脚 |
| ImportError | module not found | 安装依赖库 |

---

## 八、经验总结

### 8.1 硬件连接经验

1. **电源选择**：优先使用 3.3V，避免 5V 损坏传感器
2. **引脚选择**：使用 ADC1 通道（GPIO1-11），兼容性更好
3. **接线检查**：上电前再次确认接线正确

### 8.2 网络调试经验

1. **分段排查**：先测试 WiFi，再测试 TCP，最后测试 MQTT
2. **工具辅助**：使用 `netstat`、`ping` 等工具定位问题
3. **配置验证**：修改配置后务必重启服务验证

### 8.3 代码编写经验

1. **错误处理**：所有外部调用都应包含异常捕获
2. **日志记录**：关键节点添加日志，便于排查
3. **代码复用**：封装成类和函数，便于维护

---

## 📝 附录：常用命令

```bash
# 检查 Mosquitto 状态
netstat -ano | findstr ":1883"

# 重启 Mosquitto（管理员权限）
net stop mosquitto && net start mosquitto

# 安装 Python 库
python -m pip install paho-mqtt

# 测试网络连通性
ping 192.168.140.233
```

---

**文档版本**：v1.0  
**创建日期**：2026年5月29日  
**适用对象**：ESP32 IoT 开发者、技术支持人员

---