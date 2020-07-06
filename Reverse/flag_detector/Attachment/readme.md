# Attachment

## 文件
题目源码
```
.
├── checker
│   ├── check.c
│   ├── check.go
│   └── check.h
└── main.go
```
flag_detector为赛时的题目文件


## 使用

```bash
go build main.go 
# 编译， 产生main文件，
strip main 
# 去符号
upx main 
# upx压缩
```

## 代码思路

main.go里面主要是使用gin框架做了个简单的web服务，
check部分使用的引入的./checker里面的check.go包，这个是封装的一个c的程序，check.c为主要的程序代码，是一个栈虚拟机，有个函数调用的实现。
