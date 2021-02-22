# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
# items为数据结构模板文件
# 定义数据属性

import scrapy


class AuthorItem(scrapy.Item):
    name = scrapy.Field()
    birthdate = scrapy.Field()
    bio = scrapy.Field()
