---
title:   SCTF2020_Password Lock Plus
---

# Password Lock Plus

![](http://image.skywang.fun/picGO/20200702161851.png)

## 1.串口配置部分

查阅参考手册的第一个操作为配置USART1的波特率寄存器，且波特率为115200

![](http://image.skywang.fun/picGO/20200702161351.png)

![](http://image.skywang.fun/picGO/20200702161409.png)

第二个操作为配置USART1控制寄存器一，且配置为：使能串口&使能发送

![](http://image.skywang.fun/picGO/20200702161422.png)

发送STCF{

使用轮询发送完'STCF{'后，开启串口DMA，后续字符使用DMA发送

![](http://image.skywang.fun/picGO/20200702162202.png)

![](http://image.skywang.fun/picGO/20200702162231.png)

## 2.DMA1_通道4配置

![](http://image.skywang.fun/picGO/20200702161828.png)

1. 前两个操作为设置DMA的起始地址与目标地址(哪一个是目标在后面设置，这里为了好写提前透露外设是目标，寄存器是起始)，并且起始地址为0x20000000(在SRAM区里)，目标为USART的数据寄存器，也就是说DMA的目标是串口(串口1连接在DMA1_通道4上)

![](http://image.skywang.fun/picGO/20200702161507.png)

![](http://image.skywang.fun/picGO/20200702161519.png)

2. 地址0x48就是对应的 偏移 = 0x48 - 0x14*(4-1) = 0xC (20 = 0x14)

   0x1e操作为设置DMA传输数量与配置DMA，它配置为0x1e也就是说串口输出的有30位字符

![](http://image.skywang.fun/picGO/20200702161540.png)

 

3. 根据之前的计算方式0x44对应的偏移是:0x8

    最后一个0x492的配置, 最后一个操作为配置DMA4(16bit->8bit|储存器增量，外设非增量|储存器->外设|允许传输完成中断)

   ![](http://image.skywang.fun/picGO/20200702163137.png)

0x492对应‭010010010010‬

![](http://image.skywang.fun/picGO/20200702161630.jpg)

这里重点看一下数据宽度：

![](http://image.skywang.fun/picGO/20200702164906.png)

16bit->8bit模式意味着只会读取数组(8bit的数组)中2n的数据，2n+1的数据会被忽略掉。

```c
"t_h_1_s_1_s_n_0_t_r_1_g_h_t_f_l_a_g_"
提取之后就是th1s1sn0tr1ghtflag
```

![](http://image.skywang.fun/picGO/20200702163549.png)

在2,3,4 中断处理函数中都有对输出字符的替换, 

把上边的字符 'th1s1sn0tr1ghtflag' 挨个替换之后得到flag

```c
SCTF{that1s___r1ghtflag} //中间3个下划线
```

