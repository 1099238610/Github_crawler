# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GithubCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    issue_list = scrapy.Field()
    issue_name = scrapy.Field()
    issue_url = scrapy.Field()
    issue_status = scrapy.Field()


class ProjectItem(scrapy.Item):
    project_name = scrapy.Field()
    issues = scrapy.Field()
