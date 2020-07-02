# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AuthorQuoteItem(scrapy.Item):
    # define the fields for Quote item here
    content = scrapy.Field()
    tags = scrapy.Field()

    # define the fields for Author item here
    name = scrapy.Field()
    author_url = scrapy.Field()
