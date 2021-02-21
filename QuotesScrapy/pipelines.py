# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from common import database as db


class AuthorPipeline:
    def __init__(self):
        self.cnx, self.cursor = db.dbConnect()

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        authorDict = {
            'name': item.get('name', 'N/A'),
            'birthdate': item.get('birthdate', 'N/A'),
            'bio': item.get('bio', 'N/A'),
        }
        sql = ''
        self.cursor.execute(sql, **authorDict)
        self.cnx.commit()

    def close_spider(self, spider):
        self.cnx.close()
        self.cursor.close()


class QuotesPipeline:
    def process_item(self, item, spider):
        pass
