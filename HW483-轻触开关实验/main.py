"""
    HW483:
        针脚顺序:[SIG, VCC, GND]
        SIG: 信号针脚
        VCC: 电源针脚
        GND: 接地针脚
    参考链接: https://cloud.tencent.com/developer/inventory/1503/article/1707083
    备注: 本实验还使用了HW477-双色LED元件, 参考HW477-双色LED元件
"""
import RPi.GPIO as GPIO # 导入GPIO控制模块
import time # 导入时间模块

BtnPin = 19 # 按钮信号针脚
VCCPin = 26 # 按钮电源针脚
Rpin = 16 # LED 红色针脚
Ypin = 20 # LED 黄色针脚

def setup():
    GPIO.setmode(GPIO.BCM) # 设置针脚编码模式为BCM
    GPIO.setup(Ypin, GPIO.OUT) # 设置针脚模式为输出
    GPIO.setup(Rpin, GPIO.OUT)
    GPIO.setup(VCCPin, GPIO.OUT) 
    GPIO.output(VCCPin,GPIO.HIGH) # 设置电源针脚输出高电平
    GPIO.setup(BtnPin, GPIO.IN, pull_up_down = GPIO.PUD_UP) # 设置按钮信号针脚模式为输出, 设置上拉电阻
    # 设置事件监听，监听升降沿事件，并添加回调函数，通过添加弹跳时间消除事件抖动
    GPIO.add_event_detect(BtnPin, GPIO.BOTH, callback = detect, bouncetime=50)

# 控制LED闪烁的函数
def Led(x):
    if x == 0: # 按下按钮状态
        GPIO.output(Rpin, 1) # 点亮红色
        GPIO.output(Ypin, 0) # 关闭黄色
    if x == 1: # 松开按钮状态
        GPIO.output(Rpin, 0) # 关闭红色
        GPIO.output(Ypin, 1) # 点亮黄色

# 打印提示信息
def Print(x):
    if x == 0:
        print("************************")
        print("*      按钮已按下       *")
        print("************************")
    elif x == 1:
        print("************************")
        print("*      按钮已松开       *")
        print("************************")

# 回调函数
def detect(chn):
    Led(GPIO.input(BtnPin)) # 控制双色LED闪烁
    Print(GPIO.input(BtnPin)) # 打印提示信息

# 循环,保证程序一直执行
def loop():
    while True:
        pass # 空语句,可以后期扩展
    
def destory():
    GPIO.output(Rpin, GPIO.LOW) # 关闭红色LED
    GPIO.output(Ypin, GPIO.LOW) # 关闭黄色LED
    GPIO.output(VCCPin, GPIO.LOW) # 关闭按钮电源
    GPIO.cleanup() # 重置GPIO

if __name__ == "__main__":
    setup() # 初始化
    try:
        loop()
    except KeyboardInterrupt: # Ctrl + C 退出程序
        destory()