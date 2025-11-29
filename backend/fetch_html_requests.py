import requests
from bs4 import BeautifulSoup
import csv
from proxy_utils import load_working_proxies, make_request_with_proxy_fallback

# URL of the webpage you want to fetch
url = "https://xhamster1.desi/best/weekly"
# url = "https://quotes.toscrape.com/tag/inspirational/"

# Load working proxies
working_proxies = load_working_proxies()
print(f"Loaded {len(working_proxies)} working proxies")

# Send HTTP GET request with proxy fallback
response = make_request_with_proxy_fallback(url, working_proxies)
# Check request status
if response and response.status_code == 200:
    print("✅ Successfully fetched the webpage.")
    html = response.text
else:
    print(f"❌ Failed to fetch page. Status code: {response.status_code if response else 'No response'}")
    exit()

# Find the <title> tag manually
start_index = html.find("<title>") + len("<title>")
end_index = html.find("</title>")
title = html[start_index:end_index]

print("Page Title:", title.strip())

# Count how many <a> tags appear
# link_count = html.count("<a")

# Print results
# print(f"Number of <a> tags (links): {link_count}")

# # Parse HTML with BeautifulSoup
# soup = BeautifulSoup(response.text, "html.parser")

# # Find all quote blocks
# quotes = soup.find_all("div", class_="quote")

# # Prepare CSV file to store data
# with open("quotes.csv", "w", newline="", encoding="utf-8") as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(["Quote", "Author", "Tags"])

#     # Loop through each quote block
#     for q in quotes:
#         try:
#             text = q.find("span", class_="text").get_text(strip=True)
#         except AttributeError:
#             text = "N/A"

#         try:
#             author = q.find("small", class_="author").get_text(strip=True)
#         except AttributeError:
#             author = "N/A"

#         # Get tags (can be multiple)
#         try:
#             tag_elements = q.find_all("a", class_="tag")
#             tags = ", ".join([tag.get_text(strip=True) for tag in tag_elements])
#         except AttributeError:
#             tags = "N/A"

#         writer.writerow([text, author, tags])

print("✅ Data saved to quotes.csv")
