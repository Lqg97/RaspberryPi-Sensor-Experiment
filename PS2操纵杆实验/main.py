#!/usr/bin/env python
import PCF8591 as ADC 
import time
import sys

def setup():
    ADC.setup(0x48)                 # Setup PCF8591
    global state

def direction():    #获取操纵杆方向结果
    state = ['home', 'up', 'down', 'left', 'right', 'Button pressed']
    i = 0
    adc0 = ADC.read(0)
    adc1 = ADC.read(1)
    adc2 = ADC.read(2)

    if adc0 <= 5:
        i = 1       #up
    if adc0 >= 250:
        i = 2       #down

    if adc1 <= 5:
        i = 3       #left
    if adc1 >= 250:
        i = 4       #right

    # 由于未知原因，向左摇操纵杆会自动触发按键按下信号
    if adc2 == 0:  #所以加上ADC.read(1) >= 6这个限制，
        i = 5       # Button pressed

    if  adc0 - 125 < 15   \
    and adc0 - 125 > -15  \
    and adc1 - 125 < 15   \
    and adc1 - 125 > -15  \
    and adc2 == 255:
        i = 0         #home
    
    return state[i]

def loop():
    status = ''
    while True:
        tmp = direction()
        if tmp != None and tmp != status:
            print(tmp)     #不为空和tmp值变化时打印
            status = tmp

def destroy():
    pass      #pass语句就是空语句

if __name__ == '__main__':      # Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:   # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()