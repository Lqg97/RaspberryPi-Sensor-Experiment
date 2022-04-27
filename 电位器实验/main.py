#!/usr/bin/env python
import PCF8591 as ADC
import time

def setup():
    ADC.setup(0x48)

def loop():
    status = 1
    while True:
        print('Value:{}'.format(ADC.read(0)))  
 #读取AIN0通道上模拟信号转化成数字信号的值，范围是0~255
        Value = ADC.read(0)  #值越大，LED灯越亮
        outvalue = map(Value,0,255,50,120)
        ADC.write(outvalue)
#为AOUT模拟输出，写入数字信号值（范围0~255），会转化为相应的模拟电压输出
#但是当outvalue的值在120以下时，LED灯就基本熄灭了，所以需要map()函数转换一下
        time.sleep(0.2)
def destory():
    ADC.write(0)
    
def map(x,in_min,in_max,out_min,out_max):
#将范围是0~255的输入值转化成范围120~255的输出值
#这样转化方式也能提高控制LED亮度的精度
    return (x-in_min) * (out_max-out_min) / (in_max - in_min) +out_min
    
if __name__ == '__main__':
    try:
        setup()
        loop()
    except KeyboardInterrupt: 
        destory()