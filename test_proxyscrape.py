import requests

# Test different proxyscrape URLs to see which one works
urls = [
    "https://api.proxyscrape.com/v2/?request=get&protocol=http&timeout=5000&country=all",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=all",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
]

for url in urls:
    print(f"\n🔍 Testing: {url}")
    try:
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        content = response.text[:200]
        print(f"Content preview: {content}")
        
        # Count potential proxies
        lines = response.text.splitlines()
        proxy_count = 0
        for line in lines[:10]:  # Check first 10 lines
            line = line.strip()
            if line and ":" in line and line.split(":")[1].isdigit():
                proxy_count += 1
                print(f"  Found: {line}")
        
        print(f"Potential proxies found: {proxy_count}")
        
    except Exception as e:
        print(f"Error: {e}")
