这是一个stm32f103c8t6 MCU密码锁，它具有4个按键，分别为1、2、3、4。分别对应于GPIO_PA1，GPIO_PA2，GPIO_PA3，GPIO_PA4。

输入正确的密码, 它将通过串口(PA9--TX)发送flag.

提示: 中断向量表, 芯片数据手册. 固件没有禁用jtag, 可以进行动态调试. 对按键的触发方式有特殊要求, 自行分析.

```English
This is a stm32f103c8t6 mcu password lock, it has 4 keys respectively 1, 2, 3, 4. Corresponding to GPIO_PA1, GPIO_PA2, GPIO_PA3, GPIO_PA4. 

By entering the correct password, it sends the flag through the serial port(PA9--TX).
```

