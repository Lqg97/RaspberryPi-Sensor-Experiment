"""
    HW481:
        针脚顺序: [,R,Y]
        GND: 接地针脚
        R: 红色针脚
        Y: 绿色针脚 
    参考链接: https://cloud.tencent.com/developer/inventory/1503/article/1707063
"""

import RPi.GPIO as GPIO # GPIO控制模块
import time # 时间模块

PIN = 16
GPIO.setmode(GPIO.BCM)

if __name__=="__main__":
    try:
        GPIO.setup(PIN, GPIO.OUT) # 设置针脚模式为输出
        GPIO.output(PIN, GPIO.HIGH) # 设置针脚为高电平，启动LED灯
        while True:
            pass
    except KeyboardInterrupt: # 处理遇到用户中断(control + C)的情况
        GPIO.cleanup() # 重置GPIO状态


