"""
    倾斜开关:
        针脚顺序: [SIG, VCC, GND]
        SIG: 信号针脚
        VCC: 电源针脚
        GND: 接地针脚
"""
import RPi.GPIO as GPIO # 导入GPIO控制模块
import time # 导入时间模块

SigPin = 23
VccPin = 24
RPin = 16
YPin = 20

def setup():
    GPIO.setmode(GPIO.BCM) # 设置针脚编码为BCM
    GPIO.setup(RPin, GPIO.OUT) # 设置针脚模式为输出
    GPIO.setup(YPin, GPIO.OUT)
    GPIO.setup(VccPin, GPIO.OUT)
    GPIO.output(VccPin, GPIO.HIGH) # 设置电源针脚输出高电平
    GPIO.setup(SigPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # 设置信号针脚模式为输入, 添加上拉电阻
    GPIO.add_event_detect(SigPin, GPIO.BOTH, callback=detect, bouncetime= 50)

# 控制LED闪烁的函数
def Led(x):
    if x == 0:
        GPIO.output(RPin, 1) # 点亮红色
        GPIO.output(YPin, 0) # 关闭黄色
    if x == 1: 
        GPIO.output(RPin, 0) # 关闭红色
        GPIO.output(YPin, 1) # 点亮黄色
    
def Print(x):
    if x == 0:
        print(' *************** ')
        print(' *     倾斜    * ')
        print(' *************** ')
 
# 回调函数
def detect(chn):
    Led(GPIO.input(SigPin)) # 控制双色LED闪烁
    Print(GPIO.input(SigPin)) # 打印提示信息

# 循环,保证程序一直执行
def loop():
    while True:
        pass # 空语句,可以后期扩展
    
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