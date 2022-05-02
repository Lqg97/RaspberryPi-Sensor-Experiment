#!/usr/bin/env python

import time
import smbus  #SMBus (System Management Bus,系统管理总线) 在程序中导入“smbus”模块

BUS = smbus.SMBus(1)   #创建一个smbus实例
# 0 代表 /dev/i2c-0， 1 代表 /dev/i2c-1 ,具体看使用的树莓派那个I2C来决定
def write_word(addr, data):
    global BLEN   #该变量为1表示打开LCD背光，若是0则关闭背光
    temp = data
    if BLEN == 1:
        temp |= 0x08  #0x08=0000 1000，表开背光
        #buf |= 0x08等价于buf = buf | 0x08(按位或)
    else:
        temp &= 0xF7  #0xF7=1111 0111，表关闭背光
        #buf &= 0xF7等价于buf = buf & 0xF7(按位与)
    BUS.write_byte(addr ,temp)  #这里为什么又一次写入8位？？？？？？
    #write_byte(int addr, char val)发送一个字节到设备

def send_command(comm):
    # Send bit7-4 firstly
    buf = comm & 0xF0   #与运算，取高四位数值
    #由于4位总线的接线是接到P0口的高四位，传送高四位不用改
    buf |= 0x04    #buf |= 0x04等价于buf = buf | 0x04(按位或)0x04=0000 0100
    # RS = 0, RW = 0, EN = 1 
    #为什么这样写入代表RS = 0, RW = 0, EN = 1，低4位在这里有何意义？？？？？？？？
    write_word(LCD_ADDR ,buf)  #为什么这里又是8位写入？？？？？
    time.sleep(0.002)
    buf &= 0xFB    #buf &= 0xFB等价于buf = buf & 0xFB(按位与)0xFB=1111 1011
    # Make EN = 0，EN从1——>0，下降沿，进行写操作
    #为什么这样写入代表Make EN = 0？？？？？？？？
    write_word(LCD_ADDR ,buf)

    # Send bit3-0 secondly
    buf = (comm & 0x0F) << 4  #与运算，取低四位数值，
    #由于4位总线的接线是接到P0口的高四位，所以要再左移4位
    buf |= 0x04               
    # RS = 0, RW = 0, EN = 1 写入命令
    write_word(LCD_ADDR ,buf)
    time.sleep(0.002)
    buf &= 0xFB               # Make EN = 0
    write_word(LCD_ADDR ,buf)

def send_data(data):
    # Send bit7-4 firstly
    buf = data & 0xF0
    buf |= 0x05               # RS = 1, RW = 0, EN = 1 写入数据
    write_word(LCD_ADDR ,buf)
    time.sleep(0.002)
    buf &= 0xFB               # Make EN = 0
    write_word(LCD_ADDR ,buf)

    # Send bit3-0 secondly
    buf = (data & 0x0F) << 4
    buf |= 0x05               # RS = 1, RW = 0, EN = 1 写入数据
    write_word(LCD_ADDR ,buf)
    time.sleep(0.002)
    buf &= 0xFB               # Make EN = 0
    write_word(LCD_ADDR ,buf)

def init(addr, bl):  #LCD1602初始化
    global LCD_ADDR  #该变量为设备地址
    global BLEN      #该变量为1表示打开LCD背光，若是0则关闭背光
    LCD_ADDR = addr
    BLEN = bl
    try:
        send_command(0x33) # 必须先初始化为8行模式   110011 Initialise
        time.sleep(0.005)
        send_command(0x32) # 然后初始化为4行模式   110010 Initialise
        time.sleep(0.005)
        send_command(0x28) # 4位总线，双行显示，显示5×8的点阵字符。
        time.sleep(0.005)
        send_command(0x0C) # 打开显示屏，不显示光标，光标所在位置的字符不闪烁
        time.sleep(0.005)
        send_command(0x01) # 清屏幕指令，将以前的显示内容清除
        time.sleep(0.005)
        send_command(0x06) # 设置光标和显示模式，写入新数据后光标右移，显示不移动
        BUS.write_byte(LCD_ADDR, 0x08)  #这里这样写入0x08是什么意思？？？？？？
    except:
        return False
    else:
        return True

def clear():
    send_command(0x01) # 清屏


def write(x, y, str):
    if x < 0:   #LCD1602只有16列，2行显示，小于第0列的数据要做修正
        x = 0
    if x > 15:  #LCD1602只有16列，2行显示，大于第15列的数据要做修正
        x = 15
    if y <0:    #LCD1602只有16列，2行显示，小于第0行的数据要做修正
        y = 0
    if y > 1:   #LCD1602只有16列，2行显示，大于第1行的数据要做修正
        y = 1

    # 移动光标
    addr = 0x80 + 0x40 * y + x  
    #第一行第一位的地址为0x00，加上D7恒为1，所以第一行第一位的地址为0x80
    #第二行第一位是0x40，加上D7恒为1，所以第二行第一位的地址为0x80加上0x40，最后为0xC0
    send_command(addr)       #设置显示位置

    for chr in str:
        send_data(ord(chr))  #发送显示内容
        #ord()函数以一个字符（长度为1的字符串）作为参数，
        #返回对应的 ASCII 数值，或者 Unicode 数值

# 字符串循环显示
def wordLoop(strs):
    x = 0
    for i in range(0,2):
        if len(strs[i])>=16:
            continue
        strs[i]=strs[i].ljust(16,' ')
    print(strs)
        
    while True:
        for row in range(0,2):
            for i in range(0,16):                
                addr =  0x80 + 0x40 * row + i
                send_command(addr)
                send_data(ord(strs[row][(i+x)%len(strs[row])]))
        time.sleep(1)
        x += 1
        x %= 16      

if __name__ == '__main__':
    init(0x27, 1)  #在树莓派终端上使用命令'sudo i2cdetect -y 1'查询设备地址为0x27
    # 第二个参数1表示打开LCD背光，若是0则关闭背光
    # write(4, 0, 'Hello,')  #4，0参数指显示的起始位置为第4列，第0行
    # write(7, 1, 'World!') #7，1参数指显示的起始位置为第7列，第1行
    #‘Hello’为要显示的字符串
    try:
        wordLoop(['test programe','LQG is a coder!'])
    except KeyboardInterrupt:
        init(0x27, 1)