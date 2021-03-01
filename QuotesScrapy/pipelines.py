# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re
import pandas as pd
from datetime import datetime
from QuotesScrapy.common import database as db
from sqlalchemy import create_engine


def getDate(dateText):
    return datetime.strptime(dateText, '%B %d, %Y')


class AuthorPipeline:
    def __init__(self):
        self.cnx, self.cursor = db.dbConnect()

    def open_spider(self, spider):
        db.truncateTable(self.cnx, self.cursor, 'author')

    def process_item(self, item, spider):
        authorDict = item
        authorDict['birthdate'] = getDate(authorDict['birthdate'])
        print('name==========>', authorDict['name'])
        print('birthdate=====>', authorDict['birthdate'])
        sql = 'INSERT IGNORE INTO author (name, birthdate, bio) VALUES (%s, %s, %s)'
        authorTuple = (authorDict['name'], authorDict['birthdate'], authorDict['bio'])
        self.cursor.execute(sql, authorTuple)
        self.cnx.commit()

    def close_spider(self, spider):
        # 查询爬取的author数据
        query = 'SELECT `name`, birthdate, bio FROM author'
        self.cursor.execute(query)
        authorDataSet = self.cursor.fetchall()
        authorDataFrame = pd.DataFrame(authorDataSet, columns=['name', 'birthdate', 'bio'])
        # 剔除重复的author数据，重新导入
        authorResultSet = authorDataFrame.drop_duplicates(subset=['name', 'birthdate'])
        db.truncateTable(self.cnx, self.cursor, 'author')
        conn = create_engine(db.sqlalchemyURL)
        authorResultSet.to_sql(name='author', con=conn, if_exists='append', index=False)
        print('数据库连接已关闭')
        self.cnx.close()
        self.cursor.close()


class QuotesPipeline:
    def process_item(self, item, spider):
        pass
