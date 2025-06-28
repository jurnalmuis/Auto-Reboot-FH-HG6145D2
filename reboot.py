import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
import time

MODEM_IP = "http://192.168.1.1"
USERNAME = "user"
PASSWORD = "admin1234"
KEY_IV = b"opqrstuvwxyz{|}~"  # 16-byte IV and Key Fiberhome

# ======== ENKRIPSI ========
def fhencrypt(password):
    padded = password + chr(16 - len(password) % 16) * (16 - len(password) % 16)
    cipher = AES.new(KEY_IV, AES.MODE_CBC, iv=KEY_IV)
    encrypted = cipher.encrypt(padded.encode())
    return encrypted.hex().upper()

session = requests.Session()

# === HEADERS UNTUK LOGIN ===
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": MODEM_IP,
    "Referer": f"{MODEM_IP}/html/login_inter.html",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
}
print("\n⚡ FiberHome HG6145D2 Auto-Reboot Script")
# Step 1: Open login page
session.get(f"{MODEM_IP}/html/login_inter.html", headers=headers, verify=False)

# Step 2: Get session ID
resp = session.get(f"{MODEM_IP}/cgi-bin/ajax?ajaxmethod=get_refresh_sessionid", headers=headers, verify=False)
sessionid = resp.json().get("sessionid")
if not sessionid:
    print("[❌] Failed to get sessionid.")
    exit(1)
print(f"\n[1/4] Get Session...")
time.sleep(3)

# Step 3: Encrypt password ala modem
enc_pass = fhencrypt(PASSWORD)

# Step 4: Login
login_payload = {
    "ajaxmethod": "do_login",
    "username": USERNAME,
    "loginpd": enc_pass,
    "port": "0",
    "sessionid": sessionid,
    "_": "0.1"
}
resp = session.post(f"{MODEM_IP}/cgi-bin/ajax", headers=headers, data=login_payload, verify=False)
if "login_result" not in resp.text:
    print("[❌] Login failed.")
    exit(1)
print(f"✅ Got Session.")
print("[2/4] Try Login...")

# Step 5: Check login_user status
resp = session.get(f"{MODEM_IP}/cgi-bin/ajax?ajaxmethod=get_login_user", headers=headers, verify=False)
login_info = resp.json()
if login_info.get("session_valid") != 1 or login_info.get("login_user") not in ["1", "0"]:
    print("[-] Login user/session not valid.")
    exit(1)
# === print(f"[✅] Login valid. Session ID: {login_info.get('sessionid')}")===
time.sleep(2)
print(f"✅ Verifying user...")
time.sleep(3)
print(f"✅ Login Valid.")
print(f"[3/4] Get New Session...")
time.sleep(3)
print(f"✅ Got New Session Done.")

# === HEADERS UNTUK REBOOT ===
reboot_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": headers["User-Agent"],
    "Referer": f"{MODEM_IP}/html/reboot.html"
}

# Step 6: Reboot
reboot_url = f"{MODEM_IP}/cgi-bin/ajax?ajaxmethod=set_onu_reboot&sessionid={sessionid}&_=0.123"

time.sleep(2)
print("✅ Send Reboot...")
time.sleep(1)
resp = session.get(reboot_url, headers=reboot_headers, verify=False)

try:
    result = resp.json()
    if result.get("success") == "true":
        print("[4/4] Reboot successfully.")
    else:
        print("[❌] Reboot failed.")
        print("Response:", result)
except Exception as e:
    print("[❌] Failed to parse response.")
    print("Raw:", resp.text)
    print("Error:", e)
