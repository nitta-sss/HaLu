import requests

SESSION = requests.Session()
SESSION.trust_env = False  # ← これが超重要（環境プロキシ無視）

BASE = "http://127.0.0.1:50021"

r = SESSION.get(f"{BASE}/speakers", timeout=5)
print(r.status_code)
print(r.text[:100])
