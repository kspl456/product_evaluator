import requests
from bs4 import BeautifulSoup

#url = "https://www.amazon.in/boAt-Airdopes-141-Streaming-Bluetooth/dp/B0F8BTY6HT?pf_rd_p=d958016b-0263-452a-a1c3-eb0aa1ee2889&pf_rd_r=VCCTHY4YT39RA3KAS6C3&ref_=Jup-LapsUNrec_B0F8BTY6HT&th=1"
url=input("Enter Amazon product URL: ")
url.strip()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Accept-Language": "en-US,en;q=0.9"
}

response = requests.get(url, headers=headers)
#print("Status code:", response.status_code)
#print(response.text[:300])

soup = BeautifulSoup(response.text, "html.parser")

# 1. Product Title
title = soup.find(id="productTitle")
title_text = title.get_text(strip=True) if title else "Not found"

# 2. Price
# Price (try multiple patterns)
price = soup.select_one("span.a-price-whole")
if not price:
    price = soup.select_one("span.a-offscreen")
price_text = price.get_text(strip=True) if price else "Not found"

# Rating (try multiple patterns)
rating = soup.select_one("span.a-icon-alt")
rating_text = rating.get_text(strip=True) if rating else "Not found"


print("TITLE:", title_text)
print("PRICE:", price_text)
print("RATING:", rating_text)
