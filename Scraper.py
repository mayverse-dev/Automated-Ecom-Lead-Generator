import requests
from bs4 import BeautifulSoup
import time
import random
import csv

url = f"https://www.ebay.com/sch/i.html?_nkw=mechanical+keyboard&_sacat=0&_from=R40&_trksid=p4432023.m570.l1313"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

file = open('product_data.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(file)
writer.writerow(['Product Title', 'Price', 'Seller Name', 'Review', 'Link'])

print("Starting search:....")
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

items = soup.find_all(
    'div', class_='su-card-container su-card-container--horizontal')

links_to_process = []

for item in items[1:36]:
    try:
        link = item.find('a', class_='s-card__link')['href']
        links_to_process.append(link)
    except:
        continue
print(f"Found {len(links_to_process)} items to analyze...")

count = 1
for link in links_to_process:
    try:
        print(f"[{count}/{len(links_to_process)}] Visiting Item Page")
        product_response = requests.get(link, headers=headers)
        product_soup = BeautifulSoup(product_response.text, 'html.parser')

        title_tag = product_soup.find('h1', class_='x-item-title__mainTitle')
        title = title_tag.text.strip() if title_tag else "N/A"

        price_tag = product_soup.find('div', class_='x-price-primary')
        price = price_tag.text.strip() if price_tag else "N/A"

        seller_tag = product_soup.find(
            'div', class_='vim x-sellercard-atf_main mar-t-12')
        if seller_tag:
            seller_name = seller_tag.find(
                'span', class_='ux-textspans ux-textspans--BOLD').text
        else:
            seller_name = "N/A"

        review_tag = product_soup.find(
            'span', class_='ux-textspans ux-textspans--PSEUDOLINK')
        if review_tag:
            review_score = review_tag.text.strip()
        else:
            review_score = "N/A"

        writer.writerow([title, price, seller_name, review_score, link])
        print(f"   --> Scraped: {seller_name} ({price})")

        time.sleep(random.uniform(2, 5))

        count += 1

    except Exception as e:
        print(f"   ⚠️ Error scraping this item: {e}")
        continue

file.close()
