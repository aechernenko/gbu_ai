from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from leboard_parcer.spiders.leboard import LeboardSpider
from leboard_parcer import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeboardSpider, section='ru/moskva/nedvizhimost/prodazha/kvartiry')
    # Другие категории объявлений тоже работают, например, случайно выбрал и проверил
    # ru/sergiev_posad/odezhda_obuv_i_aksessuary/zhenskiy_garderob
    process.start()

