# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/rossiya/rabota?q=Python']

    def parse(self, response: HtmlResponse):
        vacancy_urls = response.xpath('//a[@class="item-description-title-link"]/@href').extract()
        next_page = response.xpath('//a[contains(@class, "js-pagination-next")]/@href').extract_first()
        yield response.follow(next_page, callback=self.parse)
        for vac in vacancy_urls:
            yield response.follow(vac, callback=self.parse_vacancy)

    def parse_vacancy(self, response: HtmlResponse):
        _tmp_cur = {'₽': 'RUB', '$': 'USD'}
    #     _tmp_values = response.xpath("//div[@class='_3MVeX']/span[contains(@class, '_3mfro')]/span/text()").extract()
        price = response.xpath("//span[@class='price-value-string js-price-value-string']/span[contains(@class,'js-item-price')]/text()").extract_first()

        if price:
            price = price.replace(' ', '')
        currency = response.xpath(
            "//span[@class='price-value-string js-price-value-string']/span[contains(@class,'price-value-prices-list-item-currency_sign')]/span/text()").extract_first()
        name = response.xpath("//span[@class='title-info-title-text']/text()").extract_first()
    #     name = response.xpath("//div[@class='_3MVeX']/h1/text()").extract_first()
    #     v_tmp = [int(itm.replace('\xa0', '')) for itm in _tmp_values[:-1] if itm.replace('\xa0', '').isdigit()]
        salary = {'currency': currency if currency else None,
                  'min_value': price if price else None,
                  'max_value': None
                  }
    #
    #     if salary['max_value']:
        print(1)
    #
        yield JobparserItem(name=name, salary=salary)