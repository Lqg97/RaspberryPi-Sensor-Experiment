"""
    雨滴传感器:
        针脚顺序:[VCC, GND, DO, AO]
        VCC:电源针脚
        GND:接地针脚
        DO :数字信号针脚
        AO :模拟信号针脚
    参考链接: https://cloud.tencent.com/developer/inventory/1503/article/1705774
"""
import RPi.GPIO as GPIO # 导入GPIO控制模块
import time # 导入时间模块

DO = 19 # 数字信号输入针脚
GPIO.setmode(GPIO.BCM) # 设置针脚编码模式

def setup():
    GPIO.setup(DO, GPIO.IN) # 设置针脚模式为输入

# 信息打印
def Print(x):
    if x == 1: 
        print ('')
        print ('   ***************')
        print ('   * Not raining *')
        print ('   ***************')
        print ('')
    if x == 0:
        print ('')
        print ('   *************')
        print ('   * Raining!! *')
        print ('   *************')
        print ('')

def loop():
    status = 1   #初始状态为无水，高电平，所以为1
    while True:
        print(GPIO.input(DO))  #打印数字输出DO的值（无雨为1，有雨为0）
        tmp = GPIO.input(DO)
        if tmp != status:      #滴水时DO输出为低电平，无水时为高电平
            Print(tmp)         # tmp != status即遇状态变化时，打印情况
            status = tmp
        time.sleep(2)

if __name__ == '__main__':
    try:
        setup()
        loop()
    except KeyboardInterrupt: 
        pass