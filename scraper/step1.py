import requests
from bs4 import BeautifulSoup

url = "https://www.amazon.in/dp/B0FDL5K6SV?ref_=QAHzEditorial_en_IN_7&pf_rd_r=0J8GWYXYPVFRPE4QFTWG&pf_rd_p=5853ad57-738e-4eb4-b23f-be3464f046a9&pf_rd_m=A1VBAL9TL5WCBF&pf_rd_s=merchandised-search-21&pf_rd_t=&pf_rd_i=1389401031&th=1"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
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
