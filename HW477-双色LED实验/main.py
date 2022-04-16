"""
    HW477:
        针脚顺序: [GND,R,Y]
        GND: 接地针脚
        R: 红色针脚
        Y: 黄色针脚 
    参考链接: https://cloud.tencent.com/developer/inventory/1503/article/1707063
"""

import RPi.GPIO as GPIO # GPIO控制模块
import time # 时间模块

colors = [0xFF00, 0x00FF] # 颜色列表，前两位标识红色，后两位标识黄色
pins = {'pin_R':16, 'pin_G':20} # 针脚字典，BCM编码

GPIO.setmode(GPIO.BCM) # 设置针脚编码模式为BCM
# 或者为板载模式，注意同步修改针脚字典
# GPIO.setmode(GPIO.BOARD)

# 初始化LED灯
for i in pins:
    GPIO.setup(pins[i], GPIO.OUT) # 设置针脚模式为输出
    GPIO.output(pins[i], GPIO.LOW) # 设置针脚为低电平，关闭LED灯

"""
    PWM的频率决定了输出信号中on(0)和off(1)的切换速度,频率越高,切换速度越快。
    占空比指一串理想脉冲序列中,正脉冲的持续时间与脉冲总周期的比值。通过调整LED通过电流和不通过电流的时间来控制。
"""

# 设置频率为 2k Hz
p_R = GPIO.PWM(pins['pin_R'], 2000)
p_G = GPIO.PWM(pins['pin_G'], 2000)
# 设置初始占空比为0
p_R.start(0)
p_G.start(0)

# 映射函数,将颜色刺激量映射为占空比
def map(x, in_min, in_max, out_min, out_max):
    return (x-in_min)*(out_max-out_min)/(in_max-in_min)+out_min

# 设置颜色函数
def setColor(col):
    """
        先用与运算保留对应颜色的有效位值。
        通过移位运算提取对应颜色的有效值
    """
    R_val = (col & 0xFF00) >> 8 
    G_val = (col & 0x00FF) >> 0 
    
    # 将颜色的刺激量转换为占空比对应的值
    R_val = map(R_val, 0, 255, 0, 100)
    G_val = map(G_val, 0, 255, 0, 100)
    
    # 修改占空比,调整对应颜色的亮度
    p_R.ChangeDutyCycle(R_val)
    p_G.ChangeDutyCycle(G_val)

# 循环函数
def loop():
    while True:
        for col in colors: # 遍历颜色
            setColor(col) # 设置颜色
            time.sleep(0.5) # 延时0.5s

# 销毁函数
def destory():
    p_R.stop() # 停止PWM
    p_G.stop()
    for i in pins:
        GPIO.output(pins[i], GPIO.LOW) # 关掉所有LED灯
    GPIO.cleanup() # 重置GPIO状态

if __name__=="__main__":
    try:
        loop()
    except KeyboardInterrupt: # 处理遇到用户中断(control + C)的情况
        destory()
