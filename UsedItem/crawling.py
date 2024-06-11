from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import requests

from . import DBController

session = requests.Session()
dbController = DBController.DBController()

def get_bunjang_products(itemname, max_results=10):
    browser = webdriver.Chrome()
    browser.implicitly_wait(10)
    
    url = f"https://m.bunjang.co.kr/search/products?order=score&page=1&q={itemname}"
    browser.get(url)
    
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "app")))
    
    html = browser.page_source
    html_parser = BeautifulSoup(html, 'html.parser')
    items = html_parser.find_all(attrs={'alt': '상품 이미지'})

    products = []

    for idx, item in enumerate(items):
        if idx >= max_results:
            break
        aTag = item.parent.parent
        try:
            title, price, time = None, None, None
            for i, c in enumerate(aTag.children, 0):
                if i == 1:
                    info = c.get_text(separator=';;;')
                    info = info.split(sep=';;;')
                    title = info[0]
                    price = info[1]
                    time = info[2] if len(info) > 2 else "미 확인"
                if i == 2:
                    location = c.get_text()

            link = f"https://m.bunjang.co.kr{aTag.attrs['href']}"
            img_url = item.attrs['src']

            products.append({
                'flatform': 'bunjang',
                'title': title,
                'url': link,
                'location': location,
                'price': price,
                'img_url': img_url
            })
        except Exception as e:
            print("error!!", e)

    browser.quit()
    dbController.saveItems(products)

    return products


def get_dangn_products(search, max_results=10):
    base_url = 'https://www.daangn.com/search/' + search
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = session.get(base_url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    products = []

    items = soup.select('.flea-market-article')
    for idx, item in enumerate(items):
        if idx >= max_results:
            break
        try:
            link = item.select_one('.flea-market-article-link')
            href_link = 'https://www.daangn.com/' + link.get('href') if link else None
            title = item.select_one('.article-title').text
            location = item.select_one('.article-region-name').text.strip()
            price = item.select_one('.article-price').text.strip()
            img_tag = item.select_one('.card-photo img')
            img_url = img_tag.get('src') if img_tag else None

            products.append({
                'flatform': 'dangn',
                'title': title,
                'url': href_link,
                'location': location,
                'price': price,
                'img_url': img_url
            })
        except Exception as e:
            print("error!!", e)
    return products


def get_joongna_products(search, max_results=10):
    base_url = 'https://web.joongna.com/search/' + search
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = session.get(base_url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    products = []

    items = soup.select('.group.box-border.overflow-hidden.flex.rounded-md.cursor-pointer.pe-0.pb-2.lg\\:pb-3.flex-col.items-start.transition.duration-200.ease-in-out.transform.bg-white')
    for idx, item in enumerate(items):
        if idx >= max_results:
            break
        try:
            link = item.get('href')
            href_link = 'https://web.joongna.com' + link if link else None

            title = item.select_one('.line-clamp-2.text-sm.md\\:text-base.text-heading')
            title_text = title.text if title else None

            region = item.select_one('.font-semibold.space-s-2.mt-0\\.5.text-heading.lg\\:text-lg.lg\\:mt-1\\.5')
            region_text = region.text.strip() if region else None

            price = item.select_one('.text-sm.text-gray-400')
            price_text = price.text.strip() if price else None

            img_tag = item.select_one('img')
            img_url = img_tag.get('src') if img_tag else None

            products.append({
                'flatform': 'joongna',
                'title': title_text,
                'url': href_link,
                'location': region_text,
                'price': price_text,
                'img_url': img_url
            })
        except Exception as e:
            print("error!!", e)

    return products

def get_all_products(search):
    max_results = 10
    bunjang_products = get_bunjang_products(search, max_results)
    dangn_products = get_dangn_products(search, max_results)
    joongna_products = get_joongna_products(search, max_results)
    return bunjang_products + dangn_products + joongna_products
