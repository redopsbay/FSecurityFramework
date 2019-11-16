#/usr/bin/python3

import os
import shutil
import json
import base64

mysql_password=bytes(input("Enter your mysql_password: "),encoding='utf8')

def encode(password):
	return base64.b64encode(password)

mysql_password = encode(mysql_password)
print("[*] Your encrypted password is inside the b\'encrypted-password\': %s" % mysql_password)
try:
	with open("FSecurityFramework/etc/fsecurity/encryptedpassword.txt", "wb") as file:
		file.write(mysql_password)
		print("[OK] Encrypted password is saved to encryptedpassword.txt.....")
except IOError as Error:
	print("[*] Error writing your encryptedpassword into file....")
