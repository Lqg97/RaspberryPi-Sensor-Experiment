"""
    干簧管传感器:
        针脚顺序:[SIG,GND,VCC]
        SIG:信号针脚
        GND:接地针脚
        VCC:电源针脚
    参考链接: https://cloud.tencent.com/developer/inventory/1503/article/1705770
"""

import RPi.GPIO as GPIO # 导入GPIO控制模块
import time # 导入时间模块

VccPin = 19
SigPin = 26

# 双色LED针脚
RPin = 16
YPin = 20

def setup():
    GPIO.setmode(GPIO.BCM) # 设置针脚编码模式为BCM
    # 设置针脚为输出模式
    GPIO.setup(VccPin, GPIO.OUT)
    GPIO.setup(RPin, GPIO.OUT)
    GPIO.setup(YPin, GPIO.OUT)
    # 初始化针脚
    GPIO.output(RPin, GPIO.LOW)
    GPIO.output(YPin, GPIO.LOW)
    GPIO.output(VccPin, GPIO.HIGH) # 设置供电针脚输出高电平
    # 设置输入针脚
    GPIO.setup(SigPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # 设置为输入模式，添加上拉电阻
    GPIO.add_event_detect(SigPin, GPIO.BOTH, callback = detect, bouncetime = 50) # 设置触发，添加回调函数

# LED控制函数
def LED(x):
    if x == 0: # 传感器低电平，电路联通，红灯亮
        GPIO.output(RPin, GPIO.HIGH)  
        GPIO.output(YPin, GPIO.LOW) 
    if x == 1: # 传感器低电平，电路断开，黄灯亮
        GPIO.output(RPin, GPIO.LOW)
        GPIO.output(YPin, GPIO.HIGH)

# 信息打印
def Print(x):
    if x == 0:
        print("检测到磁性")

def detect(chn):
    val = GPIO.input(SigPin)
    LED(val) # 控制LED闪烁
    Print(val) # 打印信息
    print(val) # 验证输入值

def loop():
    while True:
        pass

def destory():
    GPIO.output(VccPin, GPIO.LOW)
    GPIO.output(RPin, GPIO.LOW)
    GPIO.output(YPin, GPIO.LOW)
    GPIO.cleanup()

if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destory()
