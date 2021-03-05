import os
from QuotesScrapy.common.database import config

if __name__ == '__main__':
    # 执行SQL脚本
    os.system(f'mysql -u{config["user"]} -p{config["password"]} -D{config["database"]}<quotes.sql')
    # 顺序执行爬虫，注意执行位置要在项目根目录
    os.system('scrapy crawl author')
    os.system('scrapy crawl quotes')