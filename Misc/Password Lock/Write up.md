---
title:   SCTF2020_Password Lock
---

# 1.stm32

这道题stm32f103c8t6

首先flash容量是64k, 0x08000000起始, size为0x10000

ram大小20k, 从         0x20000000启始, size为0x5000

再了解一下stm32的运行方式, 就是在套娃, 在指定寄存器不停的填充数据, 实现指定功能

题目是按键锁， 那么肯定是有gpio输入实现按键功能， 按键输入只能是两种方式：

1.读gpio状态

2.外部中断

# 2.main函数

跟进main函数第一个0x2f0, 

![](http://image.skywang.fun/picGO/20200701202941.png)

![](http://image.skywang.fun/picGO/20200701202931.png)

并查阅外设地址, 

![](http://image.skywang.fun/picGO/20200701202921.png)

可以知道这个函数实在配置RCC, 时钟部分

可以用查表的方法, 也可以用Ghidra的插件SVD-Loader也可以实现, 原理都是一样的.

然后用这个方法给其他的未知函数快速命名

## 串口发送

![](http://image.skywang.fun/picGO/20200701203629.png)

可以定位到一个关于串口发送的函数, 把hex转字符之后可以看到'stcf{'字样

![](http://image.skywang.fun/picGO/20200701203814.png)

# 4.中断在flash里的映射

![](http://image.skywang.fun/picGO/20200702135541.png)

![](http://image.skywang.fun/picGO/20200702135604.png)

当成一样的去看就行, 所以我就没去添加

# 5. EXTI, DMA1中断处理函数

通过中断向量表查找中断服务函数地址

![](http://image.skywang.fun/picGO/20200702135616.png)

着重去看这些地址

stm32使用thumb指令, 地址+1

![](http://image.skywang.fun/picGO/20200702135626.png)

![](http://image.skywang.fun/picGO/20200702135641.png)

新建一个函数

![](http://image.skywang.fun/picGO/20200702135654.png)

# 6.分析外部中断

首先是EXTI1部分

1. 首先第一个参数, 外设地址为0x4001 0414,![](http://image.skywang.fun/picGO/20200703145903.png)

![](http://image.skywang.fun/picGO/20200703150025.png)

![](http://image.skywang.fun/picGO/20200703150434.png)

地址为0x4001 0400 + 0x14的偏移, 然后赋值2, 也就是0b10, 可以看到相当于是外部中断线1挂起, 

剩下的EXTI2, EXTI3, EXTI4也是相同操作

2. 标志位

![](http://image.skywang.fun/picGO/20200702145857.png)

下一部是开始读取ram, 需要有板子进行动态调试才行........标志位去读取按键顺序, 如果是0, 就会把标志位+1操作,否则如果如果是5, 就继续+1.....

通过观察其他的EXTI2, EXTI3, EXTI4, 可以观察到触发中断的顺序就是1442413,

再观察最后一个EXTI3函数在DMA1处偏移0x44

![](http://image.skywang.fun/picGO/20200702150323.png)

20 = 0x14 

0x44 - 0x14 * (4-1) = 0x8

![](http://image.skywang.fun/picGO/20200702150720.png)

![](http://image.skywang.fun/picGO/20200702150923.png)

使能DMA1发送flag

题目要求拿到密码就行所以flag: SCTF{1442413}

