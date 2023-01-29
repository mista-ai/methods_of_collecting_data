import scrapy
from scrapy.http import HtmlResponse
from castorama_parser.items import CastoramaParserItem
from scrapy.loader import ItemLoader

class CastoramaRuSpider(scrapy.Spider):
    name = 'castorama_ru'
    allowed_domains = ['castorama.ru']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://www.castorama.ru/catalogsearch/result/?q={kwargs.get("search")}']

    def parse(self, response: HtmlResponse):
        links = response.xpath('//a[@class="product-card__name ga-product-card-name"]/@href')
        for link in links:
            yield response.follow(link, callback=self.parse_products)

    def parse_products(self, response: HtmlResponse):
        loader = ItemLoader(item=CastoramaParserItem(), response=response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('price', '//div[@class="price-wrapper  "]//span[@class="price"]/span/span//text()')
        loader.add_xpath('photos', '//div[@class="product-media"]/div[@class="product-media__top js-top-gallery"]//img/@data-src')
        # characteristics = response.xpath('//div[@class="product-block product-specifications"]/dl[@class="specs-table js-specs-table"]')
        characteristics = self.parse_characteristics(response=response)
        loader.add_value('characteristics', characteristics)
        loader.add_value('url', response.url)
        yield loader.load_item()

        # name = response.xpath('//h1/text()').get()
        # price = response.xpath('//div[@class="price-wrapper  "]//span[@class="price"]/span/span//text()').getall()
        # photos = response.xpath('//div[@class="product-media"]/div[@class="product-media__top js-top-gallery"]//img/@data-src').getall()
        # url = response.url
        # yield CastoramaParserItem(name=name, price=price, photos=photos, url=url)

    def parse_characteristics(self, response: HtmlResponse):
        titles = response.xpath('//div[@class="product-block product-specifications"]/dl[@class="specs-table js-specs-table"]/dt/span/text()').getall()
        values = response.xpath('//div[@class="product-block product-specifications"]/dl[@class="specs-table js-specs-table"]/dd/text()').getall()
        characteristics = dict()
        for title, value in zip(titles, values):
            title = title.strip()
            value = value.strip()
            characteristics[title] = value
        return characteristics