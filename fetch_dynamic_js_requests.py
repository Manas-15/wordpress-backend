import json
from playwright.sync_api import sync_playwright, TimeoutError

url = "https://xhamster1.desi/videos/odia-hot-wife-sona-body-massage-after-sex-xhESzZC"

# Your authenticated proxy
PROXY = {
    "ip": "31.59.20.176",
    "port": "6754",
    "user": "rhvchaso",
    "pass": "t85zlhdvv9b5"
}

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

def fetch_videos():
    print(f"🌍 Using proxy: {PROXY['ip']}:{PROXY['port']}")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            slow_mo=50,
            proxy={
                "server": f"http://{PROXY['ip']}:{PROXY['port']}",
                "username": PROXY["user"],
                "password": PROXY["pass"]
            }
        )

        context = browser.new_context(
            user_agent=USER_AGENT,
            viewport={"width": 1366, "height": 768},
            ignore_https_errors=True,
        )

        page = context.new_page()

        # Test IP through proxy
        print("🔍 Checking public IP...")
        page.goto("http://api.ipify.org?format=json", wait_until="load")
        proxy_ip = page.evaluate("() => document.body.innerText")
        print(f"🧠 Proxy IP detected: {proxy_ip}\n")

        print(f"🌐 Visiting: {url}")
        page.goto(url, wait_until="networkidle")

        try:
            # page.wait_for_selector(".thumb.thumb_rel.item a", timeout=30000)
            page.wait_for_selector(".thumb-list__item a", timeout=30000)
        except TimeoutError:
            print("⚠️ No video elements found.")
            browser.close()
            return

        for _ in range(10):
            page.mouse.wheel(0, 2000)
            page.wait_for_timeout(500)

        # iterate each thumb card and extract the anchor/title/image reliably
        card_elements = page.query_selector_all(".thumb-list__item.video-thumb")
        videos = []

        for card in card_elements:
            # find the best link inside the card (title/link may live on different anchors)
            link = card.query_selector("a.video-thumb-info__name, a[data-role='thumb-link'], a.video-thumb__image-container")
            if not link:
                continue

            href = link.get_attribute("href")
            if not href or not href.startswith("http"):
                continue

            # prefer explicit attributes, fallback to aria-label or text content
            title = link.get_attribute("title") or link.get_attribute("aria-label") or link.text_content()
            title = title.strip() if title else None

            img_el = card.query_selector("img")
            thumb = None
            if img_el:
                thumb = img_el.get_attribute("data-webp") or img_el.get_attribute("src")

            videos.append({
                "title": title,
                "link": href,
                "thumbnail": thumb
            })

        # Read the existing data from the JSON file
        try:
            with open("xHamsterVideo.json", "r", encoding="utf-8") as f:
                existing_videos = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_videos = []  # In case the file does not exist or is empty

        # Merge the new videos with the existing ones
        existing_videos.extend(videos)

        # Write the combined data back to the file
        with open("xHamsterVideo.json", "w", encoding="utf-8") as f:
            json.dump(existing_videos, f, indent=4, ensure_ascii=False)

        print(f"✅ Scraped {len(videos)} new videos and appended to the existing data.")
        browser.close()

if __name__ == "__main__":
    fetch_videos()
