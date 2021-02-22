# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re
from datetime import datetime
from itemadapter import ItemAdapter
from QuotesScrapy.common import database as db


def getDate(dateText):
    return datetime.strptime(dateText, '%B %d, %Y')


class AuthorPipeline:
    def __init__(self):
        self.cnx, self.cursor = db.dbConnect()

    def open_spider(self, spider):
        self.cursor.execute('truncate table author')
        self.cnx.commit()

    def process_item(self, item, spider):
        authorDict = item
        authorDict['birthdate'] = getDate(authorDict['birthdate'])
        print('name==========>', authorDict['name'])
        print('birthdate=====>', authorDict['birthdate'])
        sql = 'INSERT INTO author (name, birthdate, bio) VALUES (%s, %s, %s)'
        authorTuple = (authorDict['name'], authorDict['birthdate'], authorDict['bio'])
        self.cursor.execute(sql, authorTuple)
        self.cnx.commit()

    def close_spider(self, spider):
        print('数据库连接已关闭')
        self.cnx.close()
        self.cursor.close()


class QuotesPipeline:
    def process_item(self, item, spider):
        pass
