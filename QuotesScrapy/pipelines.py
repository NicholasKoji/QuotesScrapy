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
    def __init__(self):
        self.cnx, self.cursor = db.dbConnect()

    def open_spider(self, spider):
        db.truncateTable(self.cnx, self.cursor, 'quote')
        # 查询author表里的所有作家
        query = 'SELECT author_id, `name` FROM author'
        authorDataSet = self.cursor.execute(query)
        authorDataFrame = pd.DataFrame(authorDataSet, columns=['author_id', 'name'])
        self.authorDataFrame = authorDataFrame

    def process_item(self, item, spider):
        quoteDict = item
        quoteDataFrame = pd.DataFrame(quoteDict)
        # 替换author name
        quoteResultSet = quoteDataFrame.merge(self.authorDataFrame, how='left')['text', 'author']
        # 重命名author_id
        # 筛选出text、author_id字段，保存quote表数据
        # 分析出quote和tag的关系数据，添加到表quote_ref_tag
        sql = 'INSERT INTO quote (text, author) VALUES (%s, %s)'
        quoteTuple = (quoteDict['text'], quoteDict['author'])
        self.cursor.execute(sql, quoteTuple)
        self.cnx.commit()

    def close_spider(self, spider):
        self.cnx.close()
        self.cursor.close()
