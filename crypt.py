#!/usr/bin/env python
# coding: utf-8

from Crypto.Cipher import AES
from Crypto import Random
import json
from StringIO import StringIO

io = StringIO()
key = b'0123456789ABCDEF'

with open("generated.json", "r") as jsondata:
	db = json.load(jsondata)
	#print(db)

print(db[0]['guid'])

print(type(db))

#exit()
jsondb = ''.join(db[0])
print(type(jsondb))
iv = Random.new().read(AES.block_size)
cipher = AES.new(key, AES.MODE_CFB, iv)
msg = iv + cipher.encrypt(str(db[0]))

print(msg)

cipher = AES.new(key, AES.MODE_CFB, iv)
dmsg = cipher.decrypt(msg)


print(dmsg[16:].decode())

