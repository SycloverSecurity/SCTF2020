# write up

## golang

golang部分主要是gin实现的一个web服务， 路由和参数：
```
/ 主页

/v1/login?name=xxx  登陆

/v2/user   初始化，产生asdf文件
/v2/flag?flag=xxx   读取flag，写入hjkl文件，且设置有默认值"this is flag"。

/v3/check  检测flag
```

## check

check部分主要转到c编写的一个虚拟机，
指令如下：
```c
typedef enum {
    nop,    	 // 0			停止虚拟机运行
    pop,     	 // 1			弹出栈顶值(栈顶指针-1)
    push,    	 // 2+var		将var压栈
    jmp,    	 // 3+var		跳转到相对偏移var的位置(var可以为负数，为向前跳转，一般为循环的结构)

    jmpf,  	 // 7+var		如果栈顶值不为0则跳转到偏移var的位置
    cmp,  	 // 8+var		比较栈顶值和var并将结果0/1压入栈。

    call,        // 10+index	        按照index索引调用对应的函数
    ret,         // 11			函数返回

// 基于栈的运算=> 将栈顶两值弹出，运算，结果压栈
    add,         // 12			加法
    sub,         // 13			减法

    xor,         // 17			异或
    
    read,        // 18			从文件./hjkl中读入flag，并转化到一个数组内。
    printc,      // 19			putchar(TOP1)
    stoA,        // 10			reg_a = TOP1
    lodA,        // 21			push reg_a
    pushflag,    // 22			push flag[TOP1]
    popflag,     // 23			flag[TOP2] = Top1
    Dpush,       // 24			push TOP1

    stoB,        // 26			reg_b = TOP1
    lodB,        // 27			push reg_b
    nopnop,      // 28			调试辅助指令
    set_var_ret  // 29 		赋值整个check的返回值， ret=reg_a
} opcode;
```

逻辑如下：
```python
# -1 10 1 10 4 10 5 2 1 20 10 3 11 -2 
def main():
	fun1()
	fun4()
	fun5()
	fun3(1)

# -1 18 11 -2 
def fun1():
	read_flag()

# -1 2 1 22 8 1 7 6 1 2 1 12 3 -11 1 2 1 13 20 11 -2 
def fun2():
	a = 1
	while(flag[a] != 1):
		a += 1
	return a-1;

# -1 29 0 11 -2 
def fun3(reg_a):
	ret = reg_a
	exit()

# -1 10 2 21 8 22 7 5 2 2 20 10 3 1 2 1 8 23 7 9 24 20 10 6 2 1 12 3 -13 11 -2 
def fun4():
	a = fun2()
	if (a != 22):
		fun3(2)
	for i in range(1, 23, 1):
		fun6(i)

''' -1 
2 1  26 2 73   20 10 7 
2 2  26 2 89   20 10 7 
2 3  26 2 70   20 10 7 
2 4  26 2 84   20 10 7 
2 5  26 2 -111 20 10 7 
2 6  26 2 116  20 10 7 
2 7  26 2 103  20 10 7 
2 8  26 2 124  20 10 7 
2 9  26 2 121  20 10 7 
2 10 26 2 102  20 10 7 
2 11 26 2 99   20 10 7 
2 12 26 2 42   20 10 7 
2 13 26 2 124  20 10 7 
2 14 26 2 77   20 10 7 
2 15 26 2 121  20 10 7 
2 16 26 2 123  20 10 7 
2 17 26 2 43   20 10 7 
2 18 26 2 43   20 10 7 
2 19 26 2 77   20 10 7 
2 20 26 2 43   20 10 7 
2 21 26 2 43   20 10 7 
2 22 26 2 111  20 10 7 
11 -2 '''
def fun5():
	fun7(1, 73)
	fun7(2, 89)
	.......

# -1 21 22 2 122 17 23 11 -2 
def fun6(a):
	flag[a] ^= 122 

# -1 10 8 27 22 21 13 8 4 7 5 2 2 20 10 3 11 -2 
def fun7(reg_b, reg_a):
	a = fun8(reg_a)
	if (flag[reg_b] - a != 4):
		fun3(2)

# -1 21 2 108 17 20 11 -2 
def fun8(reg_a):
	return reg_a ^ 108
# -2 
```
## solver

```python
arr = [73,89,70,84,-111,116 ,103,124,121,102,99,42,124,77,121,123,43,43,77,43,43,111]

print(bytes(map(lambda x: (((x ^ 108) + 4) ^ 122), arr)))
```

flag: `SCTF{functi0n_ca11_11}` 