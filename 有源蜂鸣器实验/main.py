"""
    有源蜂鸣器:
        针脚顺序:[SIG,VCC,GND]
        SIG: 信号针脚
        VCC: 电源针脚
        GND: 接地针脚
    参考链接: https://cloud.tencent.com/developer/inventory/1503/article/1705767
"""
import RPi.GPIO as GPIO # 导入GPIO控制模块
import time # 导入时间模块

SigPin = 19
VccPin = 26

def setup():
    GPIO.setmode(GPIO.BCM) # 设置针脚编码模式为BCM
    GPIO.setup(SigPin, GPIO.OUT) # 设置针脚为输出模式
    GPIO.setup(VccPin, GPIO.OUT)
    GPIO.output(SigPin, GPIO.HIGH) # 设置针脚输出高电平
    GPIO.output(VccPin, GPIO.HIGH)

def on():
    GPIO.output(SigPin, GPIO.LOW) # 低电平是响

def off():
    GPIO.output(SigPin, GPIO.HIGH) # 高电平停止响

# 间歇式蜂鸣
def beep(x):
    on()
    time.sleep(x)
    off()
    time.sleep(x)

# 循环函数
def loop():
    while True:
        beep(2)

def destory():
    GPIO.output(SigPin, GPIO.HIGH) # 设置蜂鸣器不响
    GPIO.output(VccPin, GPIO.LOW) # 关闭电源输出
    GPIO.cleanup() # 重置GPIO

if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt: # Ctrl + C 退出
        destory()
