# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GithubCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    issue_list = scrapy.Field()
    # user_name = scrapy.Field()
    # type = scrapy.Field()
    # body = scrapy.Field()
    # url = scrapy.Field()
    # datetime = scrapy.Field()
    # related_issue = scrapy.Field()
    # related_issue_link = scrapy.Field()
