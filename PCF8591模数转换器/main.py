"""
    PCF8591模数转换器:
    参考链接: https://cloud.tencent.com/developer/inventory/1503/article/1705785
"""
#!/usr/bin/env python
import PCF8591 as ADC

def setup():
    ADC.setup(0x48)

def loop():
    while True:
        print(ADC.read(0)) 
  #打印电位计电压大小A/D转换后的数字值（从AIN0借口输入的）
  #范围是0~255,0时LED灯熄灭，255时灯最亮
        ADC.write(ADC.read(0)) 
  #将0通道输入的电位计电压数字值转化成模拟值从AOUT输出
  #给LED灯提供电源VCC输入

def destroy():
    ADC.write(0)

if __name__ == "__main__":
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        destroy()