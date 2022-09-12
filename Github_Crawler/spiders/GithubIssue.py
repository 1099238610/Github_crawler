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
    start_urls = ['https://github.com/botpress/botpress/issues/5423']

    def parse(self, response):
        item = GithubCrawlerItem()

        discuss_content = response.xpath('//div[@class="js-quote-selection-container"]')

        timeline = []

        result = {}

        # add all comment data from github issue page
        self.add_comment_data(discuss_content, timeline)

        # add all timeline item data from github issue page
        self.add_timeline_item_data(discuss_content, timeline)

        result['item_list'] = timeline

        print(json.dumps(result))

    def add_comment_data(self, discuss_content, timeline):
        # get comment body data
        for item in discuss_content.xpath('//div[@class="ml-n3 timeline-comment unminimized-comment comment '
                                          'previewable-edit js-task-list-container js-comment timeline-comment--caret"]'):
            # get the user name for issue timeline
            user_name = item.xpath('.//a[@class="author Link--primary text-bold css-truncate-target "]/text()').get()

            # get the data of the timeline item
            datetime = item.xpath('.//a[@class="Link--secondary js-timestamp"]//text()').get()

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
            timeline.append(timeline_item)

    def add_timeline_item_data(self, discuss_content, timeline):

        # get timeline item body data
        for item in discuss_content.xpath('//div[@class="TimelineItem-body"]'):
            timeline_item = {}

            # get the user name for issue timeline
            user_name = item.xpath('.//a[@class="author Link--primary text-bold"]/text()').get()

            # get the data of the timeline item
            datetime = item.xpath('.//a[@class="Link--secondary"]//text()').getall()

            if datetime is not None:
                if len(datetime) > 1:
                    datetime = datetime[1]
                else:
                    datetime = datetime[0]

            # get the comment of the timeline item
            item_body = item.xpath(
                './/div[@class="Link--primary f4 text-bold markdown-title"]/a/text()').getall()

            item_type = item.xpath('text()').getall()[2].replace("\n", "").strip()

            # get related issue
            related_issue = item.xpath('.//span[@class="color-fg-muted text-normal"]/text()').get()

            timeline_item = {
                "user": user_name,
                "datetime": datetime,
                "body": item_body,
                "type": item_type,
                "related_issue": related_issue
            }

            if timeline_item["type"] == "":
                timeline_item["type"] = "mention"

            timeline.append(timeline_item)