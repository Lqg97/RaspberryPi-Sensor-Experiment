"""
    震动传感器:
        针脚顺序:[SIG, VCC, GND]
        SIG: 信号针脚
        VCC: 电源针脚
        GND: 接地针脚
    参考链接: https://cloud.tencent.com/developer/inventory/1503/article/1705759
"""
import RPi.GPIO as GPIO # 导入GPIO控制模块
import time # 导入时间模块


SigPin = 23
VccPin = 24
RPin = 16
YPin = 20

tmp = 0 # 全局临时变量

def setup():
    GPIO.setmode(GPIO.BCM) # 设置针脚编码为BCM
    GPIO.setup(RPin, GPIO.OUT) # 设置针脚模式为输出
    GPIO.setup(YPin, GPIO.OUT)
    GPIO.setup(VccPin, GPIO.OUT)
    GPIO.output(VccPin, GPIO.HIGH) # 设置电源针脚输出高电平
    GPIO.setup(SigPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # 设置信号针脚模式为输入, 设置默认值为0
   


# 控制LED闪烁的函数
def Led(x):
    if x == 0:
        GPIO.output(RPin, 1) # 点亮红色
        GPIO.output(YPin, 0) # 关闭黄色
    if x == 1: 
        GPIO.output(RPin, 0) # 关闭红色
        GPIO.output(YPin, 1) # 点亮黄色

# 打印提示信息
def Print(x):
    global tmp
    if x != tmp:
        if x == 0:
            print("************************")
            print("*         开启          *")
            print("************************")
        if x == 1:
            print("************************")
            print("*         关闭         *")
            print("************************")
        tmp = x

def loop():
    state = 0
    while True:
        if GPIO.input(SigPin):
            state = state + 1
            state = state % 2
            Led(state)
            Print(state)
            time.sleep(1)

def destory():
    GPIO.output(RPin, GPIO.LOW) # 关闭红色LED
    GPIO.output(YPin, GPIO.LOW) # 关闭黄色LED
    GPIO.output(VccPin, GPIO.LOW) # 关闭按钮电源
    GPIO.cleanup() # 重置GPIO

if __name__ == "__main__":
    setup() # 初始化
    try:
        loop()
    except KeyboardInterrupt: # Ctrl + C 退出程序
        destory()