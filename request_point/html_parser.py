import requests
import pandas as pd
import re

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


def init_driver(URL):

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-infobars")
    options.add_argument("start-maximized")
    options.add_argument("--disable-extensions")

    driver = webdriver.Chrome(options = options)
    driver.maximize_window()

    driver.get(URL)

    return driver


def parse_html(driver, URL):

    df = pd.DataFrame(columns = ['Name', 'Price', 'Description'])

    soup = BeautifulSoup(driver.page_source, 'html.parser') 
    driver.close()

    names = soup.find_all('div', class_ = 'catalog__product-title')
    names = [name.a.text for name in names]
    df['Name'] = names

    prices = soup.find_all('div', class_ = 'catalog__product-price_current')
    prices = [int(re.findall(r'\d+', price.text)[0]) for price in prices]
    df['Price'] = prices

    urls = soup.find_all('div', class_ = 'catalog__product-content')
    pages = [requests.get(URL + url.a['href']) for url in urls]

    descriptions = []
    for page in pages:

        soup = BeautifulSoup(page.text, 'html.parser')
        full_description = ''
        
        color = soup.find('div', class_ = 'product__colors-title')
        full_description += 'Цвет: ' + color.text.strip() + '\n'

        description = soup.find('div', class_ = 'product__desc')

        for child in description.children:
            full_description += child.text.strip() + '\n'
        
        descriptions.append(full_description)
        
    df['Description'] = descriptions

    return df


def parser(URL):

    #driver = init_driver(URL)
    #df = parse_html(driver, URL)

    return 'text'#df