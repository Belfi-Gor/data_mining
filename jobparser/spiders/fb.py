# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random

class FbSpider(scrapy.Spider):
    fb_login = ''
    fb_passwd = ''
    name = 'fb'
    allowed_domains = ['facebook.com']
    start_urls = ['https://www.facebook.com/']
    options = webdriver.FirefoxOptions()
    options.set_preference("permissions.default.desktop-notification", 0)
    webdriver = webdriver.Firefox(firefox_options=options)
    initial_user = 'romanchuk.s.a'
    sleep_min = 1
    sleep_max = 5

    def parse(self, response: HtmlResponse):
        self.webdriver.get('https://www.facebook.com/')
        time.sleep(random.randint(self.sleep_min, self.sleep_max))
        self.webdriver.find_element_by_xpath('//input[@type="email"]').send_keys(self.fb_login)
        self.webdriver.find_element_by_xpath('//input[@type="password"]').send_keys(self.fb_passwd)
        self.webdriver.find_element_by_xpath('//input[@type="password"]').send_keys(Keys.RETURN)
        time.sleep(random.randint(self.sleep_min, self.sleep_max))
        self.webdriver.get('https://www.facebook.com/romanchuk.s.a')
        time.sleep(random.randint(self.sleep_min, self.sleep_max))
        self.webdriver.find_element_by_xpath('//body').send_keys(Keys.PAGE_DOWN)
        self.webdriver.find_element_by_xpath('//body').send_keys(Keys.PAGE_DOWN)
        time.sleep(random.randint(self.sleep_min, self.sleep_max))
        friends_url = self.webdriver.find_element_by_css_selector('#profile_timeline_tiles_unit_pagelets_friends a')
        self.webdriver.get(friends_url.get_attribute('href'))
        time.sleep(random.randint(self.sleep_min, self.sleep_max))
        counter_old = 0
        counter_new = 1
        while counter_old < counter_new:
            self.webdriver.find_element_by_xpath('//body').send_keys(Keys.PAGE_DOWN)
            self.webdriver.find_element_by_xpath('//body').send_keys(Keys.PAGE_DOWN)
            self.webdriver.find_element_by_xpath('//body').send_keys(Keys.PAGE_DOWN)
            self.webdriver.find_element_by_xpath('//body').send_keys(Keys.PAGE_DOWN)
            time.sleep(random.randint(self.sleep_min, self.sleep_max))
            friends_profiles = self.webdriver.find_elements_by_xpath('//li/div[@class="clearfix _5qo4"]/a')
            counter_old = counter_new
            counter_new = len(friends_profiles)
            time.sleep(random.randint(self.sleep_min, self.sleep_max))

        for i in range(len(friends_profiles)):
            yield self.parse_friend(friends_profiles[i].get_attribute('href'))

    def parse_friend(self, link):
        self.webdriver.get(link)
        time.sleep(random.randint(self.sleep_min, self.sleep_max))
        self.webdriver.find_element_by_xpath('//body').send_keys(Keys.PAGE_DOWN)
        self.webdriver.find_element_by_xpath('//body').send_keys(Keys.PAGE_DOWN)
        time.sleep(random.randint(self.sleep_min, self.sleep_max))
        self.webdriver.find_element_by_xpath('//body').send_keys(Keys.PAGE_DOWN)
        self.webdriver.find_element_by_xpath('//body').send_keys(Keys.PAGE_DOWN)
        time.sleep(random.randint(self.sleep_min, self.sleep_max))
        friends_url = self.webdriver.find_element_by_css_selector('#profile_timeline_tiles_unit_pagelets_friends a')
        print(2)
        pass
# webdriver.find_elements_by_xpath(
                # '//ul[@class="media-stream"]/li/picture/source[@type="image/jpeg"]'))