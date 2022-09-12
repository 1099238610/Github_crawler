# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GithubCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    types = scrapy.Field()
    comment = scrapy.Field()
    url = scrapy.Field()
