import scrapy
from scrapy.http import HtmlResponse
from job_parser.items import JobParserItem
from scrapy.loader import ItemLoader


class HhRuSpider(scrapy.Spider):
    name = "hh_ru"
    allowed_domains = ["hh.ru"]
    start_urls = ["http://hh.ru/"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = ['https://hh.ru/search/vacancy?no_magic=true&L_save_area=true&text=machine+'
                           'learning&excluded_text=&area=1&salary=&currency_code=RUR&experience'
                           '=doesNotMatter&order_by=relevance&search_period=0&items_on_page=20']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@data-qa="pager-next"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        vacancy_links = response.xpath('//a[@data-qa="serp-item__title"]/@href').getall()
        for vacancy in vacancy_links:
            yield response.follow(vacancy, callback=self.parse_vacancy)

    def parse_vacancy(self, response: HtmlResponse):
        loader = ItemLoader(item=JobParserItem(), response=response)
        loader.add_css('name', 'h1::text')
        # loader.add_xpath('salary', '//div[@data-qa="vacancy-salary"]//text()')
        loader.add_xpath('company', '//span[@data-qa="bloko-header-2"]/text()')
        loader.add_xpath('key_skills', '//div[@class="bloko-tag-list"]//text()')
        vacancy_salary = response.xpath('//div[@data-qa="vacancy-salary"]//text()').getall()
        starts, ends, salary_currency, compensation_type = HhRuSpider.salary_normalizer(vacancy_salary)
        # print(starts, ends, salary_currency, compensation_type)
        loader.add_value('salary_from', starts)
        loader.add_value('salary_to', ends)
        loader.add_value('currency', salary_currency)
        loader.add_value('compensation_type', compensation_type)
        yield loader.load_item()

    def salary_normalizer(salary):
        starts = '-'
        ends = '-'
        currency = '-'
        compensation_type = '-'
        if 'от ' in salary:
            starts = salary[1].replace('\xa0', '')
            starts = int(starts)
        if 'до ' in salary:
            ends = salary[1].replace('\xa0', '')
            ends = int(ends)
        if ' до ' in salary:
            ends = salary[3].replace('\xa0', '')
            ends = int(ends)
        if len(salary) > 1:
            currency = salary[-3]
            compensation_type = salary[-1]
        return starts, ends, currency, compensation_type
