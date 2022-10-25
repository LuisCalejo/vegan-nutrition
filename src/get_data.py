import pandas as pd
from bs4 import BeautifulSoup
import lxml
import requests
import math

DATA_DIR = '../data/albert_heijn'
URL_PRODUCTS = 'https://www.ah.nl/producten'
URL_BASE = 'https://www.ah.nl'
PRODUCT_CATEGORIES = [
    # 'aardappel-groente-fruit', # split category into 5 to work around page limit
    # 'aardappel-groente-fruit?kenmerk=nutriscore%3Aa',
    # 'aardappel-groente-fruit?kenmerk=nutriscore%3Ab',
    # 'aardappel-groente-fruit?kenmerk=nutriscore%3Ac',
    # 'aardappel-groente-fruit?kenmerk=nutriscore%3Ad',
    # 'aardappel-groente-fruit?kenmerk=nutriscore%3Ae',
    'salades-pizza-maaltijden',
    # 'vlees-kip-vis-vega',
    # 'kaas-vleeswaren-tapas',
    # 'zuivel-plantaardig-en-eieren',
    # 'bakkerij-en-banket',
    # 'ontbijtgranen-en-beleg',
    # 'snoep-koek-chips-en-chocolade',
    # 'tussendoortjes',
    # 'frisdrank-sappen-koffie-thee',
    # 'wijn-en-bubbels',
    # 'bier-en-aperitieven',
    # 'pasta-rijst-en-wereldkeuken',
    # 'soepen-sauzen-kruiden-olie',
    # 'sport-en-dieetvoeding',
    # 'diepvries'
]


def get_product_categories(url):
    # Note: this function is not used
    product_categories = []
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")
    html = list(soup.children)[2]
    body = list(html.children)[3]
    div_app = list(body.children)[16]
    start_of_content = list(div_app.children)[1]
    div_grid_root = list(start_of_content.children)[0]
    div_row = list(div_grid_root.children)[0]
    div_column = list(div_row.children)[0]
    div_product_categories = list(div_column.children)[0]
    for item in div_product_categories:
        div_root = list(item.children)[0]
        div_category = list(div_root.children)[0]
        div_taxonomy_card = list(div_category.children)[0]
        url_product = div_taxonomy_card.parent.attrs['href']
        product_categories.append(url_product)
    return product_categories


def get_product_details(url):
    x = 1


def get_products(url):
    product_urls = []
    if 'aardappel-groente-fruit' in url:
        page_sep = '&'
    else:
        page_sep = '?'
    page = 50
    url_page = url + page_sep + 'page=' + str(page)
    res = requests.get(url_page)
    soup = BeautifulSoup(res.content, "html.parser")
    html = list(soup.children)[2]
    div_app = list(html.body.children)[16]
    div_container_root = list(div_app.children)[2]
    div_container_root_search = list(div_container_root.children)[1]
    div_search_lane_wrapper = list(div_container_root_search.children)[3]
    for div_search_lane in list(div_search_lane_wrapper.children):
        div_search_lane_class = div_search_lane.attrs['class'][0]
        if 'product-grid-lane_root' in div_search_lane_class:
            divs_products = list(div_search_lane.children)
            for div in divs_products:
                div_class = div.attrs['class'][0]
                if 'product-card-portrait' in div_class:
                    div_header_root = list(div.children)[0]
                    div_hyperlink = list(div_header_root.children)[0]
                    product_urls.append(div_hyperlink.attrs['href'])
    return product_urls


def get_product_details(url_product, cat):
    product_details['cat'] = cat
    res = requests.get(url_product)
    soup = BeautifulSoup(res.content, "html.parser")
    html = list(soup.children)[2]
    div_title = soup.find_all("div", class_="product-card-header_root__1GTl1")
    product_details['title'] = list(div_title[0].children)[0].text
    div_subtitle = soup.find_all("div", class_="product-card-header_unitInfo__2ncbP")
    product_details['subtitle'] = div_subtitle[0].text
    div_nutriscore = soup.find_all("div", class_="nutriscore_root__cYcXV product-card-hero_nutriscore__1g_JA")
    product_details['nutriscore'] = div_nutriscore[0].title
    table_nutrition = soup.find_all("table", class_="product-info-nutrition_table__1PDio")
    table_nutrition_body = list(table_nutrition[0].children)[1]
    for row in table_nutrition_body.children:
        col1 = list(row.children)[0]
        col2 = list(row.children)[1]
        product_details[col1.text] = col2.text
    div_price = soup.find_all("div", class_="price-amount_root__37xv2 product-card-hero-price_now__PlF9u")
    price = ''
    if not div_price:  ## if product has discount then container has different name
        div_price = soup.find_all("div",
                                  class_="price-amount_root__37xv2 price-amount_was__1PrUY product-card-hero-price_was__1ZNtq")
        for child in div_price[0].children:
            price += child.text
    else:  # regular product (no discount)
        for child in div_price[0].children:
            price += child.text
    product_details['price'] = price
    return product_details


cat_products = dict()
product_details = dict()

for cat in PRODUCT_CATEGORIES:
    url = URL_PRODUCTS + '/' + cat
    cat_products[cat] = get_products(url)
    for product in cat_products[cat]:
        url_product = URL_BASE + product
        product_details[product] = get_product_details(url_product, cat)

x = 1
