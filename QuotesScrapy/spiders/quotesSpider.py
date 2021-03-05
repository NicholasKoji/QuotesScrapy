import scrapy
from QuotesScrapy.items import QuotesItem


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    custom_settings = {
        'ITEM_PIPELINES': {
            'QuotesScrapy.pipelines.QuotesPipeline': 300
        }
    }

    start_urls = [
        'http://quotes.toscrape.com',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            quoteItem = QuotesItem()
            quoteItem['text'] = quote.css('span.text::text').get()
            quoteItem['author'] = quote.css('small.author::text').get()
            quoteItem['tags'] = quote.css('div.tags a.tag::text').getall()
            yield quoteItem


        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
