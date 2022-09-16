# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class GithubCrawlerPipeline:

    def process_item(self, item, spider):
        return item


class DatetimePipeline:
    """
    处理爬取的日期格式
    """
    def process_item(self, item, spider):
        for issue in item:
            if item.get("datetime"):
                datetime = item.get("datetime")
                # 如果日期不为空
                if datetime is not None:
                    if len(datetime) > 1:
                        item['datetime'] = datetime[1]
                    else:
                        item['datetime'] = datetime[0]
            return item


class JsonWriterPipeline(object):
    """
    读取每个爬取的item, 写入json文件
    """
    def __init__(self):
        # 必须使用 w+ 模式打开文件，以便后续进行 读写操作（w+模式，意味既可读，亦可写）
        # 注意：此处打开文件使用的不是 python 的 open 方法，而是 codecs 中的 open 方法
        self.json_file = codecs.open(BASE_DIR + '/result/issue_data.json', 'w+', encoding='UTF-8')

    def open_spider(self, spider):
        """
        预写入json格式符号
        :param spider:
        :return:
        """
        # self.json_file.write('{ \n')
        # self.json_file.write('  "issue_list": \n')
        self.json_file.write('[\n')

    def process_item(self, item, spider):
        """
        写入数据到文件
        :param item: 爬取的对象
        :param spider:
        :return: 爬取数据对象
        """
        print(item)
        # 为使得 Json 文件具有更高的易读性，辅助输出 '\n'（换行符）
        item_json = json.dumps(dict(item), ensure_ascii=False, indent=4)
        self.json_file.write(item_json + ',\n')
        return item

    def close_spider(self, spider):
        """
        处理并关闭文件
        :param spider:
        :return:
        """
        self.json_file.seek(-2, os.SEEK_END)
        # 使用 truncate() 方法，将后面的数据清空
        self.json_file.truncate()

        # 重新输出'\n'，并输入']'，与 open_spider(self, spider) 时输出的 '['，构成一个完整的数组格式
        self.json_file.write('\n]')
        # self.json_file.write('\n}')

        # 关闭文件
        self.json_file.close()
