import urllib.request
import os
import time

BASE = "https://web.bale.ai"
DEST = "/Users/kookoo/Documents/bale/test"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36",
    "Cookie": "_ga=GA1.1.914523929.1772883250; _ym_uid=1772883546748868436; _ym_d=1772883546; access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE4MDQwNjMwNjUsImlhdCI6MTc3Mjk1OTA2NSwiaXNzIjoiaHR0cHM6Ly93ZWIuYmFsZS5haSIsInBheWxvYWQiOnsiYXBwX2lkIjo0LCJhdXRoX2lkIjoiNTI0MDk2MTExNTAxODM1OTQxMiIsImF1dGhfc2lkIjoxMzEzNTQ5ODk4LCJzZXJ2aWNlIjoid2ViX2xpdGUiLCJ1c2VyX2lkIjozNTUzMjE1NjN9fQ.0x8EWpzTkcSugYxbkiu6FPfMitrwnwt-YZA7b6u0-XYmnuN7VBXetHMlNXkm04YbNKrpliqaCuRkXp3xyR3fgL9_JMdJIh26rZ6tJV-1cplxUmZAfM5mTxCD0BkNBSPYly-yZ9Q0V9fe4diVzDsSJrZyyjPFUu8JyFU-jFyShmaRAmL-FtQ8fCvAYGWEt36eCL5hXSP8Sjykmj4eANYwv8uFKkzQNVo6gNJuVmRAc-yHBOS3OeYIUc46uowLrZDSLfR92Ss2fx4_vZBsYkCd-_eamoVhXFjOvTUU6B36CCRoGCG2fnwV2ASyNoy1Mq5XwxQxpNetGPmdyPRUS8GnbiTUbB9w-ePBX48xG2Gjn_anZ4uiyhK-6fejGJWhJeq6-U6p6fLfjxYTR0toq7NKhMvAXEVVfz_9xKtIqhhjMkWeps2muDNw4zroTBNEgl_wsp3U3bpOcbcINbNaXrX1602VrCc3sxy223jDJeq5iI_zX0ymsaZHTRrVKM7OvVH6RM3aTFNiHRkVLhwwBnXZmQUADQl6OwNO7mHqqLe87aL4PiouNCSyUKOSA0E_buNPCKS5WII1GtW__bHs9Km6MzbwViHE3dpxpqQMYfPEKfInuIP3a9Yt-4i4W4snw_wHNEHKYrQ-kbllzKK17DxQV9Lgk8qH4sdQJCVt38OT19c; _ym_isad=2"
}

# All files discovered from service-worker.js
FILES = [
    # HTML entry points
    "/index.html",
    "/enroll.html",
    "/hub.html",
    "/redirecting.html",
    # Main JS bundles
    "/static/js/index.52867891.js",
    "/static/js/2028.6a01a431.js",
    "/static/js/6448.d550bfc3.js",
    "/static/js/6591.a44597be.js",
    "/static/js/7932.2d979425.js",
    "/static/js/enroll.08575865.js",
    "/static/js/hub.49e3d77d.js",
    "/static/js/redirecting.b52c30be.js",
    "/static/js/rlottie-wasm.js",
    # Service worker
    "/service-worker.js",
    "/site.webmanifest",
    "/robots.txt",
]

# Fetch the service worker to get the full async chunk list
def get_sw_chunks():
    url = BASE + "/service-worker.js"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            content = r.read().decode("utf-8", errors="replace")
        import re
        chunks = re.findall(r'(/static/js/async/[^\'"]+\.js)', content)
        main = re.findall(r'(/static/js/[^\'"]+\.js)', content)
        css = re.findall(r'(/static/css/[^\'"]+\.css)', content)
        return list(set(chunks + main + css))
    except Exception as e:
        print(f"Could not fetch SW for chunk list: {e}")
        return []

def download(path):
    url = BASE + path
    local = DEST + path
    os.makedirs(os.path.dirname(local), exist_ok=True)
    if os.path.exists(local):
        print(f"  skip (exists): {path}")
        return True
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            data = r.read()
        with open(local, "wb") as f:
            f.write(data)
        print(f"  OK ({len(data):,} bytes): {path}")
        return True
    except Exception as e:
        print(f"  FAIL: {path} — {e}")
        return False

print("Fetching async chunk list from service worker...")
extra = get_sw_chunks()
all_files = list(set(FILES + extra))
print(f"Total files to download: {len(all_files)}")

ok = fail = 0
for path in sorted(all_files):
    if download(path):
        ok += 1
    else:
        fail += 1
    time.sleep(0.05)

print(f"\nDone: {ok} downloaded, {fail} failed")
