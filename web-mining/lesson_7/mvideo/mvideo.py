from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from hashlib import sha1
import json

chrome_options = Options()

# chrome_options.add_argument('--headless')

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.mvideo.ru/')

print('Открыта главная страница')

# кликаем по контейнеру, в котором содержатся "хиты продаж"
# чтобы поле зренеия переместилось на него, и все содержимое
# хитов продаж прогрузилось
driver.find_elements_by_class_name("gallery-layout")[1].click()

# находим кнопку next
nxt_btn = driver.find_elements_by_class_name('sel-hits-button-next')[1]

# пока кнопка next активна (не имеет класса 'disabled')
# кликаем по этой кнопке (тогда в html-код подгружаются новые "хиты продаж")
while nxt_btn.get_attribute('class').find('disabled') == -1:
    nxt_btn.click()

# парсим данные со всех прогруженных "хитов продаж"
hits = driver.find_elements_by_xpath('//ul[@class="accessories-product-list"]')[1].find_elements_by_xpath('//li//h4/a')

data = [{} for _ in hits]
for hit, dat in zip(hits, data):
    json_hit = json.loads(hit.get_attribute('data-product-info'))
    dat['name'] = json_hit['productName']
    dat['price'] = json_hit['productPriceLocal']
    dat['category'] = json_hit['productCategoryName']
    dat['vendor'] = json_hit['productVendorName']
    dat['link'] = hit.get_attribute('href')
    dat['_id'] = sha1((dat['name']+dat['link']+dat['price']).encode('utf-8')).hexdigest()
    dat['price'] = float(dat['price'])

client = MongoClient('localhost', 27017)
for item in data:
    try:
        client['mvideo']['hits'].insert_one(item)
    except DuplicateKeyError:
        pass
