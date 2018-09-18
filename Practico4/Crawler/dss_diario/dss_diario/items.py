# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DssDiarioItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    categoria = scrapy.Field()
    titulo = scrapy.Field()
    copete = scrapy.Field()
    cuerpo = scrapy.Field()
    hits = scrapy.Field()
