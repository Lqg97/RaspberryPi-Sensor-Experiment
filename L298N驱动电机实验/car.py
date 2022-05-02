import RPi.GPIO as GPIO          
from time import sleep

# 右轮驱动
in1 = 23 
in2 = 24
ena = 25
# 左轮驱动
in3 = 20
in4 = 16
enb = 21
# 速度
low = 30
medium = 60
high = 90

global left,right
global forward
# 初始化
def setup():
    global forward 
    global left,right
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(in1,GPIO.OUT)
    GPIO.setup(in2,GPIO.OUT)
    GPIO.setup(ena,GPIO.OUT)
    GPIO.setup(in3,GPIO.OUT)
    GPIO.setup(in4,GPIO.OUT)
    GPIO.setup(enb,GPIO.OUT)
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)
    right = GPIO.PWM(enb, 100)
    left = GPIO.PWM(ena, 100)
    right.start(low)
    left.start(low)
    forward = True

def control(x):
    global forward 
    global left,right
    if x == 'z':
        print("run")
        left.ChangeDutyCycle(medium)
        right.ChangeDutyCycle(medium)
        if forward:
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)
            GPIO.output(in3,GPIO.HIGH)
            GPIO.output(in4,GPIO.LOW)
            print("forward")
        else:
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.HIGH)
            GPIO.output(in3,GPIO.LOW)
            GPIO.output(in4,GPIO.HIGH)
            print("backward")
    if x == 'f':
        forward = True
        control('z')
    if x == 'b':
        forward = False
        control('z')

    if x == 's':
        print('slow')
        left.ChangeDutyCycle(low)
        right.ChangeDutyCycle(low)
    if x == 'm':
        print('medium')
        left.ChangeDutyCycle(medium)
        right.ChangeDutyCycle(medium)
    if x == 'h':
        print('high')
        left.ChangeDutyCycle(high)
        right.ChangeDutyCycle(high)
    if x == 'l':
        print('left')
        left.ChangeDutyCycle(0)
        right.ChangeDutyCycle(medium)
    if x == 'r':
        print('right')
        left.ChangeDutyCycle(medium)
        right.ChangeDutyCycle(0)
    
def destory():
    GPIO.cleanup()

def loop():
    while True:
        x = input()
        if x == 'e':
            break
        control(x)
    destory()

if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destory()