如其名，这个题确实是easy..
通过查找字符串的方法找到的虚假main函数里将`isdebug`段置1然后调用`IsDebuggerPresebt`结束函数
真正的主要逻辑是通过crc32校验出来的值解密dll，并`memload`调用dll
dll内部的实现了一个aes加密以及一些简单的位运算
脚本如下
```python
from Crypto.Cipher import AES

enc = [142, 56, 81, 115, 166, 153, 42, 240, 218, 213, 106, 145, 233, 78, 152, 206, 42, 183, 61, 64, 241, 229, 29, 171, 239, 238, 176, 214, 20, 11, 42, 149]

for i in range(len(enc)):
    enc[i] ^= 0x55

for i in range(21, 28):
    p = (enc[i] & 0xaa)>>1
    q = (enc[i]<<1) & 0xaa
    enc[i] = (p|q)^0xad

for i in range(14, 21):
    p = (enc[i] & 0xcc)>>2
    q = (enc[i]<<2) & 0xcc
    enc[i] = (p|q)^0xbe

for i in range(7, 14):
    p = (enc[i] & 0xf0)>>4
    q = (enc[i]<<4) & 0xf0
    enc[i] = (p|q)^0xef

#print (enc)
cipher = enc
key = b"5343544632303230"
key = list(key)
cipher = bytes(cipher)
key = bytes(key)
aes = AES.new(key, mode=AES.MODE_ECB)
flag = aes.decrypt(cipher)

print (flag)
#SCTF{y0u_found_the_true_secret}
```
