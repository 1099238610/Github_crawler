import json

import scrapy
from Github_Crawler.items import GithubCrawlerItem


def write_html(response):
    """
    add the current page into a HTML doc
    :param response: the url response
    """
    with open("issue_timeline.html", 'w') as f:
        f.write(response)


def cobine_words(word_list):
    result = ""
    for word in word_list:
        result += word
    return result


class IssueSpider(scrapy.Spider):
    name = 'issue'
    allowed_domains = ["github.com"]

    # 放入所有需要爬取的网址
    start_urls = ['https://github.com/botpress/botpress/issues/5423']

    def parse(self, response):
        scrapy_item = GithubCrawlerItem()

        discuss_content = response.xpath('//div[@class="js-quote-selection-container"]')

        timeline = []

        result = {}

        for item in discuss_content.xpath('//div[@class="ml-n3 timeline-comment unminimized-comment comment '
                                          'previewable-edit js-task-list-container js-comment timeline-comment--caret"]'):
            # add all comment data from github issue page
            result_item = self.add_comment_data(item, timeline, scrapy_item)

            yield result_item
            # get timeline item body data
        for item in discuss_content.xpath('//*[@class="TimelineItem-body"]'):

            # add all timeline item data from github issue page
            result_item = self.add_timeline_item_data(item, timeline, scrapy_item)
            yield result_item

        result['item_list'] = timeline



    def add_comment_data(self, item, timeline, scrapy_item):
        # get comment body data

        # get the user name for issue timeline
        user_name = item.xpath('.//a[@class="author Link--primary text-bold css-truncate-target "]/text()').get()

        # get the data of the timeline item
        datetime = item.xpath('.//a[@class="Link--secondary js-timestamp"]//text()').getall()

        # get the comment of the timeline item
        comment = item.xpath(
            './/td[@class="d-block comment-body markdown-body  js-comment-body"]/p/text()').getall()
        comment = cobine_words(comment)

        item_type = item.xpath('.//h3[@class="f5 text-normal"]/text()').getall()[1].replace("\n", "").strip()

        # get related issue
        related_issue = item.xpath('.//span[@class="color-fg-muted text-normal"]/text()').get()

        timeline_item = {
            "user": user_name,
            "datetime": datetime,
            "body": comment,
            "type": item_type,
            "related_issue": related_issue
        }

        scrapy_item['user_name'] = user_name
        scrapy_item['datetime'] = datetime
        scrapy_item['body'] = comment
        scrapy_item['type'] = item_type
        scrapy_item['related_issue'] = related_issue
        # scrapy_item['related_issue_link'] = related_issue_link

        timeline.append(timeline_item)

        return scrapy_item

    def add_timeline_item_data(self, item, timeline, scrapy_item):

        # get the user name for issue timeline
        user_name = item.xpath('.//a[@class="author Link--primary text-bold"]/text()').get()

        # get the data of the timeline item
        datetime = item.xpath('.//a[@class="Link--secondary"]//text()').getall()

        # get the comment of the timeline item
        item_body = item.xpath(
            './/div[@class="Link--primary f4 text-bold markdown-title"]/a/text()').getall()

        item_type = item.xpath('text()').getall()[2].replace("\n", "").strip()

        # get related issue
        related_issue = item.xpath('.//span[@class="color-fg-muted text-normal"]/text()').get()

        related_issue_link = item.xpath('.//a//@href').getall()

        item_type, related_issue_link = self.parse_link_type(item_type, related_issue_link)

        timeline_item = {
            "user": user_name,
            "datetime": datetime,
            "body": item_body,
            "type": item_type,
            "related_issue": related_issue,
            "related_issue_link": related_issue_link
        }

        if timeline_item["type"] == "":
            timeline_item["type"] = "mention"

        scrapy_item['user_name'] = user_name
        scrapy_item['datetime'] = datetime
        scrapy_item['body'] = item_body
        scrapy_item['type'] = item_type
        scrapy_item['related_issue'] = related_issue
        scrapy_item['related_issue_link'] = related_issue_link

        timeline.append(timeline_item)

        return scrapy_item

    def parse_link_type(self, item_type, related_issue_link):
        if related_issue_link is not None:
            if len(related_issue_link) > 1:
                related_issue_link = "https://github.com/" + related_issue_link[3]
                if "pull" in related_issue_link:
                    item_type = "pull"
                if "issue" in related_issue_link:
                    item_type = "issue"
            else:
                related_issue_link = None
        return item_type, related_issue_link
