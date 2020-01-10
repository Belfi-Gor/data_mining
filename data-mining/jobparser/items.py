# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


def cleaner_photo(values):
    if values[:2] == '//':
        return f'http:{values}'
    return values

def cleaner_data(values):
    values = values.replace(' ', '')
    if '\xa0м²' in values:
        return float(values.replace('\xa0м²', ''))
    if '6' in values:
        return int(values.replace('6-комнатные', '6'))
    if '5' in values:
        return int(values.replace('5-комнатные', '5'))
    if '4' in values:
        return int(values.replace('4-комнатные', '4'))
    if '3' in values:
        return int(values.replace('3-комнатные', '3'))
    if '2' in values:
        return int(values.replace('2-комнатные', '2'))
    if '1' in values:
        return int(values.replace('1-комнатные', '1'))
    if 'студии' in values:
        return float(values.replace('студии', '0.5'))



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


class AvitoRealEstate(scrapy.Item):
    _id = scrapy.Field()
    photos = scrapy.Field(input_processor=MapCompose(cleaner_photo))
    title = scrapy.Field(output_processor=TakeFirst())
    floor = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(cleaner_data))
    house_floors = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(cleaner_data))
    house_type = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(cleaner_data))
    rooms = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(cleaner_data))
    total_s = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(cleaner_data))
    living_s = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(cleaner_data))
    kitchen_s = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(cleaner_data))
