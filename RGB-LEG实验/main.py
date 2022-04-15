"""
    RGB-LED:
        针脚顺序:[R,G,B,GND]
        R: 红色针脚
        G: 绿色针脚
        B: 蓝色针脚
        GND: 接地
    参考链接: https://cloud.tencent.com/developer/inventory/1503/article/1707072
"""

import RPi.GPIO as GPIO # 导入GPIO控制模块
import time # 时间模块

# 颜色列表
colors = [0xFF0000, 0x00FF00, 0x0000FF, 0xFF00FF, 0X00FFFF, 0xFFFF00]

# 定义针脚编号
R = 21
G = 20
B = 16

def setup(Rpin, Gpin, Bpin):
    global pins # 定义全局变量
    global p_R, p_G, p_B
    pins = {'pin_R': Rpin, 'pin_G': Gpin, 'pin_B': Bpin}
    # 设置针脚编码模式
    GPIO.setmode(GPIO.BCM)
    # 初始化LED
    for i in pins:
        GPIO.setup(pins[i], GPIO.OUT) # 设置针脚模式为输出
        GPIO.output(pins[i], GPIO.LOW) # 设置针脚输出为低电平
    # 设置脉冲频率
    p_R = GPIO.PWM(pins['pin_R'], 2000)
    p_G = GPIO.PWM(pins['pin_G'], 1999)
    p_B = GPIO.PWM(pins['pin_B'], 5000)
    # 初始化占空比
    p_R.start(0)
    p_G.start(0)
    p_B.start(0)

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def off():
    # 关闭所有led
    for i in pins:
        GPIO.output(pins[i], GPIO.LOW)

def setColor(col):
    # 提取单独的颜色值
    R_val = (col & 0xFF0000) >> 16
    G_val = (col & 0x00FF00) >> 8
    B_val = (col & 0x0000FF) >> 0
    # 将颜色值转化为占空比
    R_val = map(R_val, 0, 255, 0, 100)
    G_val = map(G_val, 0, 255, 0, 100)
    B_val = map(B_val, 0, 255, 0, 100)
    # 更改占空比
    p_R.ChangeDutyCycle(R_val)
    p_G.ChangeDutyCycle(G_val)
    p_B.ChangeDutyCycle(B_val)

def loop():
    while True:
        for col in colors:
            setColor(col)
            time.sleep(1)

def destory():
    p_R.stop()
    p_G.stop()
    p_B.stop()
    off()
    GPIO.cleanup()

if __name__ == "__main__":
    try:
        setup(R, G, B)
        loop()
    except KeyboardInterrupt:
        destory()