程序是python写的，这一点可以从IDA打开后<kbd>shift</kbd>+<kbd>f12</kbd>打开Strings Window看出来，各种`py`开头的字符串遍地走。细心一点可以确认这是pyinstaller打包而不是py2exe。

先使用[pyinstxtractor](https://github.com/extremecoders-re/pyinstxtractor)解开，还原Python代码。命令：`python pyinstxtractor.py signin.exe`

目录`\signin.exe_extracted`下，使用uncompyle6获得`main.pyc`源码。（值得注意的是，pyinstxtractor解开的时候有显示是**python38**！如果在python37环境下使用uncompyle6则可能不能得到完整的代码。

根据main.py自行反编译需要的pyc文件。可以看出程序是PyQt5写得，**程序启动时释放了一个DLL**，退出时删除。所以可以运行时把tmp.dll复制出去分析。

可以看到（看下面代码注释）：

```python
# main.py
# ....
class AccountChecker:

    def __init__(self):
        self.dllname = './tmp.dll'
        self.dll = self._AccountChecker__release_dll()
        self.enc = self.dll.enc

        # 这里已经表明调用dll中的 enc 函数，
        # 函数名参数类型和返回值都体现出来了，分析dll就方便很多了
        self.enc.argtypes = (c_char_p, c_char_p, c_char_p, c_int)
        self.enc.restype = c_int

        self.accounts = {b'SCTFer': b64decode(b'PLHCu+fujfZmMOMLGHCyWWOq5H5HDN2R5nHnlV30Q0EA')}
        self.try_times = 0
# ....
```

整体逻辑就是调用dll对用户名和密码进行加密，返回python部分进行校验。dll里面enc的逻辑比较简单，参数分别是

```
username, password, safe_password_recv, buffersize
```

有需要的话可以使用类似下面的代码进行对dll的调试

```c
#include <stdio.h>
#include <Windows.h>

int main() {
    HMODULE module = LoadLibraryA(".\\enc.dll");
    if (module == NULL) {
        printf("failed to load");
        return 1;
    }

    typedef int(*EncFun)(char*, char*, char*, int);
    EncFun enc;
    enc = (EncFun)GetProcAddress(module, "enc");

    char username[20] =  "SCTFer" };
    char pwd[33] = { "SCTF{test_flag}" };
    char recv[33] = { 0 };
    printf("%d",enc(username, pwd, recv, 32));
    return 0;
}
```

加密逻辑不是很复杂（crc64 + xor），这里不再赘述，注意字节序就好，解题脚本如下：

```python
from base64 import *
import struct

def u_qword(a):
    return struct.unpack('<Q', a)[0]

def p_qword(a):
    return struct.pack('<Q', a)

username = list(b'SCTFer')
enc_pwd = list(b64decode(b'PLHCu+fujfZmMOMLGHCyWWOq5H5HDN2R5nHnlV30Q0EA'))[:-1] # remove the last '\0'
for i in range(32):
    enc_pwd[i] ^= username[i % len(username)]

qwords = []
for i in range(4):
    qwords.append(u_qword(bytes(enc_pwd[i*8: i*8 + 8])))

for i in range(4):
    qword = qwords[i]
    for _ in range(64):
        if qword & 1 == 1:
            # 如果最低位是1，说明加密时左移后，
            # 和12682219522899977907进行了异或
            qword ^= 12682219522899977907
            qword >>= 1
            qword |= 0x8000000000000000
            continue
        else:
            qword >>= 1
    # print(qword)
    qwords[i] = qword

pwd = []
for i in range(4):
    pwd.append(p_qword(qwords[i]).decode())

flag = ''.join(pwd)
print(flag)
```

得到flag `SCTF{We1c0m3_To_Sctf_2020_re_!!}`

## DLL源码

```c
#include "enc.h"
#include <string.h>


unsigned __int64 b(unsigned __int64 a);
unsigned __int64 d(unsigned __int64 a);


int enc(char* username, char* password, char* safepwd_recv, int size) {
    int pwdlen = strlen(password);
    int namelen = strlen(username);
    if (pwdlen > size) {
        return 1;
    }

    while (pwdlen < 32) {
        password[pwdlen++] = &#39;\0&#39;;
    }

    int offset = 0;
    for (int i = 0; i < 4; i++) {
        char tmp[8] = { 0 };
        memcpy(tmp, password + offset, 8);
        *(__int64*)tmp = d(*(unsigned __int64*)tmp);
        memcpy(safepwd_recv + offset, tmp, 8);
        offset += 8;
    }

    for (int j = 0; j < 32; j++) {
        safepwd_recv[j] ^= username[j % namelen];
    }

    safepwd_recv[32] = 0;

    return 0;
}

unsigned __int64 b(unsigned __int64 a) {
    return a & 18446744073709551615ULL;
}

unsigned __int64 d(unsigned __int64 a) {
    for (int i = 0; i < 64; i++) {
        if (a & 0x8000000000000000) {
            a <<= 1;
            a = b(a ^ 12682219522899977907ULL);
            continue;
        }
        a <<= 1;
        a = b(a);
    }

    return a;
}

// -------------------------------------------
// ehc.h
#ifndef EXPORT_DLL
#define EXPORT_DLL _declspec(dllexport)
#endif // !EXPORT_DLL

EXPORT_DLL int enc(char* username, char* password, char* safepwd_recv, int size);
```