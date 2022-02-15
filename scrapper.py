import requests
import time
from bs4 import BeautifulSoup


URL = 'https://www.tottus.cl/tucapel-arroz-risotto-italiano-20235299/p/'

page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
img = soup.find("div", class_="jsx-4104767650 jsx-2423832485 product-mobileoktopshop-section")
ean = soup.find('div', class_="jsx-273525516")

print(img.prettify())