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
        item['birthdate'] = getDate(item['birthdate'])
        print('name==========>', item['name'])
        print('birthdate=====>', item['birthdate'])
        sql = 'INSERT IGNORE INTO author (name, birthdate, bio) VALUES (%s, %s, %s)'
        authorTuple = (item['name'], item['birthdate'], item['bio'])
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
        self.cnx.close()
        self.cursor.close()


class QuotesPipeline:
    def __init__(self):
        self.cnx, self.cursor = db.dbConnect()
        self.conn = create_engine(db.sqlalchemyURL)

    def open_spider(self, spider):
        db.truncateTable(self.cnx, self.cursor, 'quote')
        db.truncateTable(self.cnx, self.cursor, 'tag')
        db.truncateTable(self.cnx, self.cursor, 'quote_ref_tag')
        # 初始化tag结果集、quotes数据
        self.tagResultSet = pd.DataFrame(columns=['tag'])
        self.quotesRefData = pd.DataFrame(columns=['text', 'tag'])
        # 查询author表里的所有作家，添加到self方便匹配author id
        query = 'SELECT author_id, `name` FROM author'
        self.cursor.execute(query)
        authorDataSet = self.cursor.fetchall()
        self.authorDataFrame = pd.DataFrame(authorDataSet, columns=['author_id', 'name'])

    def process_item(self, item, spider):
        quotesDataFrame = pd.DataFrame(data=item.values(), index=item.keys()).T
        quoteDataFrame = quotesDataFrame[['text', 'author']]
        # 匹配author name
        quoteResultSet = quoteDataFrame.merge(self.authorDataFrame, how='left', left_on='author', right_on='name')
        # 提取列text、author
        quoteDataSet = quoteResultSet[['text', 'author_id']]
        # 保存quote表数据，转成tuple导入。使用to_sql效率太低并且是pandas是用不同的SQL连接，会出问题
        quoteDataTuple = quoteDataSet.to_records(index=False).tolist()[0]
        sql = 'INSERT IGNORE INTO quote (text, author_id) VALUES (%s, %s)'
        self.cursor.execute(sql, quoteDataTuple)
        self.cnx.commit()
        # 叠加tag数据
        tagDataFrame = pd.DataFrame(item['tags'], columns=['tag'])
        self.tagResultSet = self.tagResultSet.append(tagDataFrame)
        # 叠加quotesRef数据
        quotesRefDataFrame = pd.DataFrame({'text': item['text'], 'tag': item['tags']})
        self.quotesRefData = self.quotesRefData.append(quotesRefDataFrame)

    def close_spider(self, spider):
        # 剔除重复的tag数据后保存
        tagDataSet = self.tagResultSet.drop_duplicates(subset=['tag'])
        tagDataSet.to_sql(name='tag', con=self.conn, if_exists='append', index=False)
        # 分析quote和tag的关系数据，添加到表quote_ref_tag
        self.cursor.execute('SELECT text, quote_id FROM quote')
        quoteIdData = self.cursor.fetchall()
        quoteIdDataFrame = pd.DataFrame(quoteIdData, columns=['text', 'quote_id'])
        quotesRefResultSet = self.quotesRefData.merge(quoteIdDataFrame, how='left', on='text')
        self.cursor.execute('SELECT tag, tag_id FROM tag')
        tagIdData = self.cursor.fetchall()
        tagIdDataFrame = pd.DataFrame(tagIdData, columns=['tag', 'tag_id'])
        quotesRefResultSet = quotesRefResultSet.merge(tagIdDataFrame, how='left', on='tag')
        quotesRefDataSet = quotesRefResultSet[['quote_id', 'tag_id']]
        quotesRefDataSet.to_sql(name='quote_ref_tag', con=self.conn, if_exists='append', index=False)

        self.cnx.close()
        self.cursor.close()
