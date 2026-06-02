@echo off
echo 启动 Mosquitto MQTT Broker 监听所有接口...
echo.

:: Mosquitto 安装路径
set "MOSQUITTO_PATH=D:\Mosquitto"

if not exist "%MOSQUITTO_PATH%\mosquitto.exe" (
    echo 错误: 找不到 mosquitto.exe 在 %MOSQUITTO_PATH%
    pause
    exit /b 1
)

:: 创建配置文件
echo listener 1883 > "%MOSQUITTO_PATH%\mosquitto_custom.conf"
echo allow_anonymous true >> "%MOSQUITTO_PATH%\mosquitto_custom.conf"

echo 使用配置文件: "%MOSQUITTO_PATH%\mosquitto_custom.conf"
echo 监听端口: 1883 (所有接口)
echo.

:: 启动 Mosquitto
"%MOSQUITTO_PATH%\mosquitto.exe" -c "%MOSQUITTO_PATH%\mosquitto_custom.conf"