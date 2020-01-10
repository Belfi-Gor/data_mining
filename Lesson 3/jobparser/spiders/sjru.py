# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Python&geo%5Bc%5D%5B0%5D=1']

    def parse(self, response:HtmlResponse):
        next_page = response.css("a.f-test-link-dalshe::attr(href)").extract_first()

        yield response.follow(next_page, callback=self.parse)

        vacancy = response.css("div.f-test-vacancy-item div._2g1F- a._1QIBo::attr(href)").extract()
        for link in vacancy:
            yield response.follow(link, callback=self.vacancy_parse)
        pass

    def vacancy_parse(self, response: HtmlResponse):
        name = response.css("div._3MVeX h1._3mfro::text").extract_first()
        salary = ''.join(response.css("div._3MVeX span._2Wp8I::text").extract())
        company = response.css("h2.PlM3e::text").extract_first()
        yield JobparserItem(name=name, salary=salary, company=company)

