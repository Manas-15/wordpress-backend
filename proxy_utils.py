# proxy_utils.py
import json
import requests
import time
from typing import List, Optional

# NECESSARY CORRECTION 1: Populate PROXY_SOURCES with real URLs.
# These URLs typically provide plain text lists of IP:PORT format.
PROXY_SOURCES = [
    # Note: Free proxy lists change constantly and often have short lifespans.
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http"
]

WORKING_FILE = "working_proxies.json"

def fetch_free_proxies(limit: int = 20) -> List[str]:
    """Fetch free proxies from multiple online sources."""
    proxies = set()
    print(f"🌍 Fetching first {limit} free proxies...")
    
    for url in PROXY_SOURCES:
        try:
            # Use a User-Agent to avoid being blocked by some proxy list providers
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                count_before = len(proxies)
                proxy_count = 0
                
                # Debug: Show first few lines of response
                lines = response.text.splitlines()
                print(f"📄 First 3 lines from response: {lines[:3]}")
                
                for line in lines:
                    # Break if we've reached the limit
                    if len(proxies) >= limit:
                        break
                        
                    line = line.strip()
                    # Check for IP:PORT format (same logic as test script)
                    if line and ":" in line and line.split(":")[1].isdigit():
                        proxies.add(line)
                        proxy_count += 1
                        print(f"  Found: {line}")  # Debug: show found proxies
                
                newly_added = len(proxies) - count_before
                print(f"✅ Loaded {newly_added} new proxies from {url} (Total: {len(proxies)})")
                
                # Break if we've reached the limit across all sources
                if len(proxies) >= limit:
                    print(f"🎯 Reached limit of {limit} proxies")
                    break
            else:
                print(f"⚠️ Source {url} returned status {response.status_code}")
        except Exception as e:
            print(f"❌ Failed to fetch from {url}: {e.__class__.__name__}")
            
    print(f"\n--- Total discovered proxies: {len(proxies)} ---")
    return list(proxies)[:limit]  # Ensure we don't exceed the limit

def test_single_proxy(proxy: str, test_url: str = "https://httpbin.org/ip", timeout: int = 7) -> bool:
    """Test if a single proxy is working."""
    
    # CORRECTION 2: The proxy URL in 'requests' must include the scheme (http://)
    # The proxy string should be in IP:PORT format.
    proxy_url = f"http://{proxy}"
    proxies = {"http": proxy_url, "https": proxy_url}
    
    try:
        # Use verify=False to ignore SSL errors common with free HTTP proxies
        response = requests.get(test_url, proxies=proxies, timeout=timeout, verify=False)
        
        # Check status code and optionally, check if the returned IP matches the proxy IP 
        # (A quick way to filter out transparent proxies, though not done here for simplicity)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        # Catch all requests-related exceptions (Timeout, ConnectionError, etc.)
        return False

def load_existing_proxies(file_path: str = WORKING_FILE) -> List[str]:
    """Load existing working proxies from JSON file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Ensure the loaded data is a list of strings
            return [p for p in data.get("working_proxies", []) if isinstance(p, str)]
    except FileNotFoundError:
        print(f"⚠️ {file_path} not found, starting fresh.")
        return []
    except json.JSONDecodeError:
        print(f"❌ Error decoding JSON from {file_path}, starting fresh.")
        return []

def save_working_proxies(working: List[str], total_discovered: int):
    """Save working proxies to JSON."""
    data = {
        "total_discovered": total_discovered,
        "total_working": len(working),
        "working_proxies": working,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    # Improvement: Add error handling for file writing
    try:
        with open(WORKING_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"💾 Saved {len(working)} working proxies to {WORKING_FILE}")
    except IOError as e:
        print(f"❌ Error saving to file {WORKING_FILE}: {e}")

def update_proxy_list():
    """Fetch fresh proxies and save them directly to working_proxies.json (no health check)."""
    # Step 1: Load existing proxies
    old_proxies = set(load_existing_proxies())
    print(f"\n🧾 Loaded {len(old_proxies)} existing proxies")

    # Step 2: Fetch new free proxies (first 20)
    new_proxies = set(fetch_free_proxies(limit=20))
    
    # IMPROVEMENT: Prioritize testing new proxies and then re-testing old ones
    proxies_to_test = list(new_proxies.union(old_proxies))
    
    print(f"🌐 Total unique proxies to test: {len(proxies_to_test)}")

    # Step 3: Save all proxies without testing (health check commented out)
    # Comment: Proxy health check removed - saving all fetched proxies directly
    working = proxies_to_test  # Save all proxies without testing
    
    # COMMENTED OUT: Health check section
    # DELAY_BETWEEN_CHECKS = 0.5 
    # 
    # for i, proxy in enumerate(proxies_to_test, 1):
    #     print(f"🔍 [{i}/{len(proxies_to_test)}] Testing {proxy} ...", end=" ")
    #     
    #     # Test the proxy
    #     if test_single_proxy(proxy):
    #         print("✅")
    #         working.append(proxy)
    #     else:
    #         print("❌")
    #         
    #     time.sleep(DELAY_BETWEEN_CHECKS)
    
    print(f"📦 Saving all {len(working)} proxies without health check")

    # Step 4: Save results
    save_working_proxies(working, total_discovered=len(proxies_to_test))
    print("🎉 Proxy update complete!")

# Run directly
if __name__ == "__main__":
    # Suppress InsecureRequestWarning from requests due to verify=False
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    update_proxy_list()