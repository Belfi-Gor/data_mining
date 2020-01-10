# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field()
    salary = scrapy.Field()
    company = scrapy.Field()

class InsJPItem(scrapy.Item):
    _id = scrapy.Field()
    user_name = scrapy.Field()
    post_shortcode = scrapy.Field()
    post_comments = scrapy.Field()
    post_likes = scrapy.Field()
