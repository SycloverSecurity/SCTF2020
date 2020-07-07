# 出题思路
首先很明显这是一个指令抽取壳，dex文件中指令丢失，在so中还原。  
用到的是`inline-hook`,hook`libdvm.so`的`dexFindClass`,在加载类时进行指令还原

抽取的指令,和一些字符串进行加密保存，在`.init`段进行了自解密，算法为rc4,密钥为`havefun`

指令还原后完整的dex执行逻辑为,将`SCTF`类的`b`字段作为密钥,将输入的字符串进行`xxtea`加密后与`SCTF`类的`c`字段比较

值得注意的是在`JNI_OnLoad()`时替换了`SCTF`中的`b`,`c`字段

# 解题方法
1. 硬逆so层，还原字节码
2. 众所周知，app既然要运行起来，代码必将加载到内存。所以可以在适当时间将完整的dex从内存中dump出来  
本题可在`d.a.c`的`public static String a(String arg1, String arg2, String arg3)`方法里`o1`方法执行后`o2`方法执行前将dex dump

# FLAG
SCTF{y04_f1n6_th3_s3cr37}
