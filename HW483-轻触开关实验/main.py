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

BtnPin = 19
VCCPin = 26
Rpin = 16
Ypin = 20

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Ypin, GPIO.OUT)
    GPIO.setup(Rpin, GPIO.OUT)
    GPIO.setup(VCCPin, GPIO.OUT)
    GPIO.output(VCCPin,GPIO.HIGH)
    GPIO.setup(BtnPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(BtnPin, GPIO.BOTH, callback = detect, bouncetime=50)

def Led(x):
    if x == 0:
        GPIO.output(Rpin, 1)
        GPIO.output(Ypin, 0)
    if x == 1:
        GPIO.output(Rpin, 0)
        GPIO.output(Ypin, 1)

def Print(x):
    if x == 0:
        print("************************")
        print("*      按钮已按下       *")
        print("************************")
    elif x == 1:
        print("************************")
        print("*      按钮已松开       *")
        print("************************")

def detect(chn):
    Led(GPIO.input(BtnPin))
    Print(GPIO.input(BtnPin))

def loop():
    while True:
        pass
    
def destory():
    GPIO.output(Rpin, GPIO.LOW)
    GPIO.output(Ypin, GPIO.LOW)
    GPIO.output(VCCPin, GPIO.LOW)
    GPIO.cleanup()

if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destory()