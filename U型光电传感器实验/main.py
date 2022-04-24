"""
    U型光电传感器:
        针脚顺序:[SIG,GND,VCC]
        SIG:信号针脚
        GND:接地针脚
        VCC:电源针脚
    参考链接: https://cloud.tencent.com/developer/inventory/1503/article/1705774
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
    GPIO.setup(VccPin, GPIO.OUT) # 设置电源针脚模式为输出
    GPIO.setup(RPin, GPIO.OUT) # 设置LED针脚模式为输出
    GPIO.setup(YPin, GPIO.OUT)
    GPIO.output(RPin, GPIO.LOW) # 设置初始电平
    GPIO.output(YPin, GPIO.LOW)
    GPIO.output(VccPin, GPIO.HIGH)
    # 设置信号输入触发
    GPIO.setup(SigPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(SigPin, GPIO.BOTH, callback=detect, bouncetime = 50)

# LED控制函数
def LED(x):
    if x == 0: # 传感器低电平，电路联通，红灯亮 | 没有遮挡
        GPIO.output(RPin, GPIO.HIGH)  
        GPIO.output(YPin, GPIO.LOW) 
    if x == 1: # 传感器低电平，电路断开，黄灯亮 | 有遮挡
        GPIO.output(RPin, GPIO.LOW)
        GPIO.output(YPin, GPIO.HIGH)

def Print(x):
    if x == 1:
        print('    *************************')
        print('    *       光线被遮挡       *')
        print('    *************************')

def detect(chn):
    val = GPIO.input(SigPin)
    LED(val)  #控制双色LED灯闪烁的函数
    Print(val)    #打印光线被遮挡提示消息

def loop():
    while True:
        pass  #pass语句就是空语句

def destroy():
    GPIO.output(VccPin, GPIO.LOW)
    GPIO.output(YPin, GPIO.LOW)       # Green led off
    GPIO.output(RPin, GPIO.LOW)       # Red led off
    GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()