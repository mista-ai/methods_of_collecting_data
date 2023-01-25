import scrapy
from scrapy.http import HtmlResponse
from parser_job.items import ParserJobItem

class HhRuSpider(scrapy.Spider):
    name = 'hh_ru'
    allowed_domains = ['hh.ru']
    #allowed_domains = ['carrick.ru']
    start_urls = [
        'https://hh.ru/search/vacancy?area=113&search_field=name&search_field=description&only_with_salary=true&text=machine+learning&no_magic=true&L_save_area=true&items_on_page=20'
        #'https://carrick.ru/page/1'
        ]

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        
        vacancies_links = response.xpath("//a[@data-qa='serp-item__title']/@href").getall()
        for link in vacancies_links:
            yield response.follow(link, callback=self.parse_vacancy)
    
    def parse_vacancy(self, response: HtmlResponse):
        vacancy_name = response.css("h1::text").get()
        vacancy_url = response.url
        vacancy_salary = response.xpath('//div[@data-qa="vacancy-salary"]//text()').getall()
        starts, ends, salary_currency = HhRuSpider.salary_normalizer(vacancy_salary)

        yield ParserJobItem(
            name = vacancy_name, 
            url = vacancy_url,
            salary_from = starts,
            salary_to = ends,
            currency = salary_currency
        )
        
        #print('\n*************************\n%s\n*************************\n'%response.url)
    
    def salary_normalizer(salary):
        starts = None
        ends = None
        currency = None
        if 'от ' in salary:
            starts = salary[1].replace('\xa0', '')
            starts = int(starts)
        if 'до ' in salary:
            ends = salary[1].replace('\xa0', '')
            ends = int(ends)
        if ' до ' in salary:
            ends = salary[3].replace('\xa0', '')
            ends = int(ends)
        currency = salary[-3]
        print(starts, ends, currency)
        return starts, ends, currency