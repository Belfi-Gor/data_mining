# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import AvitoRealEstate
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class ZillowSpider(scrapy.Spider):
    name = 'zillow'
    allowed_domains = ['zillow.com']
    start_urls = ['https://www.zillow.com/fort-worth-tx/']
    webdriver = webdriver.Firefox()

    #def __init__(self):
        #self.webdriver = webdriver.Firefox()
        #super().__init__(self)

    def parse(self, response: HtmlResponse):
        real_estate_list = response.css('div#grid-search-results ul.photo-cards li article a.list-card-link::attr(href)')
        next = response.css(".zsg-pagination-next a::attr(href)").extract_first()
        yield response.follow(next, callback=self.parse)

        for adv in real_estate_list.extract():
            yield self.parse_adv(adv)

    def parse_adv(self, link):
        self.webdriver.get(link)
        media = self.webdriver.find_element_by_css_selector('.ds-media-col')
        photos_ul = self.webdriver.find_elements_by_css_selector('.ds-media-col ul.media-stream li')
        photo_pic_img = self.webdriver.find_elements_by_xpath(
            '//ul[@class="media-stream"]/li/picture/source[@type="image/jpeg"]')
        while len(photos_ul) > (len(photo_pic_img)-5):
            media.send_keys(Keys.PAGE_DOWN)
            photo_pic_img = self.webdriver.find_elements_by_xpath(
                '//ul[@class="media-stream"]/li/picture/source[@type="image/jpeg"]')
        print(self.webdriver.title, self.webdriver.current_window_handle)
        return None