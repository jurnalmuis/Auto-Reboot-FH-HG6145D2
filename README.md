
# 🔁 FiberHome HG6145D2 Auto Reboot Script

Skrip Python ini digunakan untuk **me-reboot modem FiberHome HG6145D2** secara otomatis melalui antarmuka web-nya.  
Tanpa perlu klik manual di browser—cukup jalanin skrip ini, modem akan reboot.

> ⚠️ *Didesain untuk jaringan lokal, gunakan dengan akun yang memiliki hak akses login.*

---

## 🔧 Requirement

- Python 3.6+
- Library:
  - `requests`
  - `pycryptodome`

Install dependency:
```bash
pip install requests pycryptodome
```

---

## 🚀 Cara Pakai

1. Edit file:
   - Ubah `MODEM_IP`, `USERNAME`, dan `PASSWORD` sesuai modem kamu.

2. Jalankan:
```bash
python reboot.py
```

Contoh output:
```
⚡ FiberHome HG6145D2 Auto-Reboot Script

[1/4] Get Session...
✅ Got Session.
[2/4] Try Login...
✅ Verifying user...
✅ Login Valid.
[3/4] Get New Session...
✅ Got New Session Done.
✅ Send Reboot...
[4/4] Reboot successfully.
```

---

## 🛠 Konfigurasi

| Parameter     | Keterangan                              |
|---------------|------------------------------------------|
| `MODEM_IP`    | IP modem lokal (default: 192.168.1.1)    |
| `USERNAME`    | Username login modem                     |
| `PASSWORD`    | Password login modem                     |
| `KEY_IV`      | Key + IV AES 16-byte (standar FiberHome) |

---

## ⚠️ Disclaimer

Use at your own risk.  
Skrip ini hanya untuk penggunaan lokal dan edukasi.  
Kami tidak bertanggung jawab atas penggunaan yang menyalahgunakan perangkat ISP.

---

## 📄 Lisensi

MIT License

Copyright (c) 2025 jurnalmuis

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
