#python2
#pip install pycrypto
import sys
import base64
import uuid
from random import Random
import subprocess
from Crypto.Cipher import AES

key  =  "kPH+bIxk5D2deZiIxcaaaA=="
mode =  AES.MODE_CBC
IV   = uuid.uuid4().bytes
encryptor = AES.new(base64.b64decode(key), mode, IV)

payload=base64.b64decode(sys.argv[1])
BS   = AES.block_size
pad = lambda s: s + ((BS - len(s) % BS) * chr(BS - len(s) % BS)).encode()
payload=pad(payload)

print(base64.b64encode(IV + encryptor.encrypt(payload)))