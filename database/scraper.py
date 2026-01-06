import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone

import json
import os
from urllib.parse import urlparse

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9"
}

def detect_platform(url):
    domain = urlparse(url).netloc.lower()

    if "amazon" in domain:
        return "Amazon"
    elif "flipkart" in domain:
        return "Flipkart"
    elif "myntra" in domain:
        return "Myntra"
    elif "ebay" in domain:
        return "eBay"
    else:
        return "Unknown"

def scrape_product(url):
    response = requests.get(url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find(id="productTitle")
    title_text = title.get_text(strip=True) if title else None

    price = soup.select_one("span.a-price-whole") or soup.select_one("span.a-offscreen")
    price_text = price.get_text(strip=True) if price else None

    rating = soup.select_one("span.a-icon-alt")
    rating_text = rating.get_text(strip=True) if rating else None

    product_record = {
        "product_url": url,
        "product_title": title_text,
        "price": price_text,
        "rating": rating_text,
        "scrape_timestamp": datetime.now(timezone.utc).isoformat(),
        "platform": detect_platform(url)
    }

    return product_record

DATASET_FILE = "dataset_raw.json"

def save_to_dataset(record):
    data = []

    if os.path.exists(DATASET_FILE):
        try:
            with open(DATASET_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            # File exists but is empty or corrupted
            data = []

    data.append(record)

    with open(DATASET_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 🔹 Run
#url = "https://www.amazon.in/Samsung-Moonlight-Storage-Gorilla-Upgrades/dp/B0FN7W26Q8/?_encoding=UTF8&pd_rd_w=NN65q&content-id=amzn1.sym.5fdfed10-663e-40d6-810e-08029e8435c0%3Aamzn1.symc.96b8365e-3b12-433f-a173-648d41788658&pf_rd_p=5fdfed10-663e-40d6-810e-08029e8435c0&pf_rd_r=2DPQQHCX8YDEEH9ZDZ0G&pd_rd_wg=ipX2E&pd_rd_r=87aa1fce-a164-42e8-8336-fb7fac1c1ef8&ref_=pd_hp_d_btf_ci_mcx_mr_hp_atf_m&th=1"
url=input("Enter Amazon product URL: ")
url.strip()
record = scrape_product(url)
save_to_dataset(record)

print("Dataset entry added:")
print(record)
