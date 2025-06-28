import requests
from Crypto.Cipher import AES
import hashlib
import json

MODEM_IP = "http://192.168.1.1"
USERNAME = "user"
PASSWORD = "user1234"

def int_aes_iv():
    return ''.join([chr(0x6f + i) for i in range(16)])  # "opqrstuvwxyz{|}~"

def pkcs7_pad(data):
    pad_len = 16 - (len(data) % 16)
    return data + chr(pad_len) * pad_len

def encrypt_password(plain):
    key = int_aes_iv().encode('utf-8')
    iv = key
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = pkcs7_pad(plain).encode('utf-8')
    encrypted = cipher.encrypt(padded)
    return encrypted.hex()

session = requests.Session()

HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": MODEM_IP,
    "Referer": f"{MODEM_IP}/html/login_inter.html",
    "User-Agent": "Mozilla/5.0"
}

# Step 1: Visit login page to establish session cookie
print("[*] Accessing login page...")
session.get(f"{MODEM_IP}/html/login_inter.html", headers=HEADERS, verify=False)

# Step 2: Get session ID
resp = session.get(f"{MODEM_IP}/cgi-bin/ajax?ajaxmethod=get_refresh_sessionid", headers=HEADERS, verify=False)
try:
    sessionid = resp.json()["sessionid"]
    print(f"[+] Got sessionid: Done")
except:
    print("[-] Failed to get sessionid")
    exit(1)

# Step 3: Encrypt password
enc_pass = encrypt_password(PASSWORD)
print(f"[+] Encrypted password: Done")

# Step 4: Send login
login_payload = {
    "ajaxmethod": "do_login",
    "username": USERNAME,
    "loginpd": enc_pass,
    "port": "0",
    "sessionid": sessionid,
    "_": "0.1"
}

login_url = f"{MODEM_IP}/cgi-bin/ajax"

print("[*] Sending login request...")
resp = session.post(login_url, headers=HEADERS, data=login_payload, verify=False)

if "login_result" not in resp.text:
    print("[-] Login failed.\n", resp.text)
    exit(1)
print("[+] Login successful.")

# Step: Get new session ID before reboot (very important!)
resp = session.get(f"{MODEM_IP}/cgi-bin/ajax?ajaxmethod=get_refresh_sessionid", headers=HEADERS, verify=False)
try:
    new_sessionid = resp.json()["sessionid"]
    print(f"[+] Got fresh sessionid for reboot: Done")
except:
    print("[-] Failed to get new sessionid for reboot.")
    exit(1)

# Step 6: Reboot
reboot_payload = {
    "ajaxmethod": "set_onu_reboot",
    "sessionid": new_sessionid,
    "_": "0.42"
}

reboot_resp = session.post(f"{MODEM_IP}/cgi-bin/ajax", headers=HEADERS, data=reboot_payload, verify=False)

if "success" in reboot_resp.text:
    print("[+] Reboot triggered.")
else:
    print("[-] Reboot failed.")
    print("Response:", reboot_resp.text)
