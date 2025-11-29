import requests
import json
import time

# Paste proxies here in format:
# IP:PORT:USERNAME:PASSWORD
PROXIES = [
    "142.111.48.253:7030:rhvchaso:t85zlhdvv9b5"
]

HTTP_TEST_URL = "http://api.ipify.org?format=json"
HTTPS_TEST_URL = "https://api.ipify.org?format=json"

TIMEOUT = 7

working_http = []
working_https = []
failed = []


def format_proxy(proxy_entry):
    """Convert IP:PORT:USER:PASS into user:pass@ip:port"""
    ip, port, user, pwd = proxy_entry.split(":")
    return f"{user}:{pwd}@{ip}:{port}"


def test_proxy(proxy_entry):
    proxy = format_proxy(proxy_entry)
    proxy_url = f"http://{proxy}"
    proxies = {"http": proxy_url, "https": proxy_url}

    print(f"\n🔍 Testing proxy: {proxy}")

    # Test HTTP
    try:
        r = requests.get(HTTP_TEST_URL, proxies=proxies, timeout=TIMEOUT)
        if r.status_code == 200:
            print(f"   ✅ HTTP OK → {r.text}")
            working_http.append(proxy)
        else:
            print(f"   ❌ HTTP FAIL → Status {r.status_code}")
    except Exception as e:
        print(f"   ❌ HTTP ERROR → {e}")

    # Test HTTPS
    try:
        r = requests.get(HTTPS_TEST_URL, proxies=proxies, timeout=TIMEOUT)
        if r.status_code == 200:
            print(f"   🔒 HTTPS OK → {r.text}")
            working_https.append(proxy)
        else:
            print(f"   ❌ HTTPS FAIL → Status {r.status_code}")
    except Exception as e:
        print(f"   ❌ HTTPS ERROR → {e}")
        failed.append(proxy)


if __name__ == "__main__":
    print("🚀 Starting proxy test...\n")

    for proxy_entry in PROXIES:
        test_proxy(proxy_entry)
        time.sleep(0.5)

    print("\n\n==============================")
    print("🟩 Working HTTP proxies:", len(working_http))
    print("🟦 Working HTTPS proxies:", len(working_https))
    print("🟥 Total failed:", len(failed))
    print("==============================")

    # Save results
    with open("working_http_proxies.json", "w") as f:
        json.dump(working_http, f, indent=4)

    with open("working_https_proxies.json", "w") as f:
        json.dump(working_https, f, indent=4)

    with open("failed_proxies.json", "w") as f:
        json.dump(failed, f, indent=4)

    print("\n📄 Files saved:")
    print(" - working_http_proxies.json")
    print(" - working_https_proxies.json")
    print(" - failed_proxies.json")
