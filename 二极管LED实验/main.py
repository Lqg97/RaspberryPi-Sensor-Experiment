"""
    二极管LED:
        针脚顺序: [+,-]
        +: 正极针脚
        -: 负极针脚, 接地
        
"""
import RPi.GPIO as GPIO # GPIO控制模块
import time # 时间模块

GPIO.setmode(GPIO.BCM) # 设置针脚编码模式为BCM

PIN = 4 # 设置针脚编码
GPIO.setup(PIN, GPIO.OUT) # 设置针脚模式为输出

# 循环闪烁LED
for i in range(1,5):
    GPIO.output(PIN, GPIO.HIGH) # 设置针脚输出高电平，点亮LED
    time.sleep(0.5) # 延时0.5s
    GPIO.output(PIN, GPIO.LOW) # 设置针脚输出低电平，关闭LED
    time.sleep(0.5) 

GPIO.cleanup() # 重置GPIO状态
