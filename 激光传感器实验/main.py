"""
    激光传感器:
    针脚顺序: [SIG,GND,VCC]
    SIG: 信号针脚
    GND: 接地针脚
    VCC: 电源针脚
    参考链接: https://cloud.tencent.com/developer/inventory/1503/article/1707079
"""
import RPi.GPIO as GPIO # 导入GPIO控制模块
import time # 导入时间模块

LedPin = 21 # 信号输出针脚

# 初始化
def setup():
    GPIO.setmode(GPIO.BCM) # 设置针脚编码方式为BCM
    GPIO.setup(LedPin, GPIO.OUT) # 设置针脚模式为输出
    GPIO.output(LedPin, GPIO.LOW) # 设置针脚输出为低电平

def loop():
    while True:
        print("... 激光关闭")
        GPIO.output(LedPin, GPIO.LOW) # 设置针脚输出低电平，激光关闭
        time.sleep(0.5)
        print("... 激光开启")
        GPIO.output(LedPin, GPIO.HIGH) # 设置针脚输出高电平，激光开启
        time.sleep(0.5)
    
def destory():
    GPIO.output(LedPin, GPIO.LOW) # 关闭激光
    GPIO.cleanup() # 重置GPIO

if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt: # Ctrl + C 退出程序
        destory()