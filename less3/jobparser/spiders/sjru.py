# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Python']

    def parse(self, response:HtmlResponse):
        # next_page = response.css("a.f-test-link-dalshe::attr(href)").extract_first()

        # yield response.follow(next_page, callback=self.parse)

        vacancy = response.css('div.f-test-vacancy-item a._1QIBo::attr(href)').extract()
        for link in vacancy:
            yield response.follow(link, callback=self.vacancy_parse)
        pass

    def vacancy_parse(self, response: HtmlResponse):
        name = response.css("div.vacancy-title  h1.header::text").extract_first()
        salary = response.css("div.vacancy-title  p.vacancy-salary::text").extract_first()
        yield JobparserItem(name=name, salary=salary)

