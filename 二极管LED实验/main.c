/*
    二极管LED:
        针脚顺序: [+,-]
        +: 正极针脚
        -: 负极针脚, 接地
        
*/


#include<wiringPi.h> // 引入GPIO控制模块头文件
#include<stdio.h> // 标准输入输出流
#define Pin 25 // 设置正极针脚, 模式为wPi

int main(){
    // 判断GPIO是否设置成功
    if(wiringPiSetup()<0){ 
        sprintf("%s","启动失败");
        return 1;
    }
    // 设置针脚为输出模式
    pinMode(Pin, OUTPUT);
    // 循环闪烁LED
    for(int i=0;i<10;i++){
        digitalWrite(Pin,1); // 设置针脚输出高电平，点亮LED
        delay(200);          // 延时 200 ms
        digitalWrite(Pin,0); // 设置针脚输出低电平，关闭LED
        delay(200);
    }
    return 0;
}

// 编译语句
// gcc -o main main.c -lwiringPi
// 运行语句
// ./main