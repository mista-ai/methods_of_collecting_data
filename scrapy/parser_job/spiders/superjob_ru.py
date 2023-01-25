import scrapy
from scrapy.http import HtmlResponse
from parser_job.items import ParserJobItem


class SuperjobRuSpider(scrapy.Spider):
    name = 'superjob_ru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[contains(@class, 'f-test-button-dalshe')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        
        vacancies_links = response.xpath("//span[contains(@class, '_2KHVB')]/a[contains(@class, '_1IHWd')]/@href").getall()
        for link in vacancies_links:
            yield response.follow(link, callback=self.parse_vacancy)
    
    def parse_vacancy(self, response: HtmlResponse):
        vacancy_name = response.css("h1::text").get()
        vacancy_url = response.url
        vacancy_salary = response.xpath("//span[@class='_4Gt5t _3Kq5N']//text()").getall()
        starts, ends, salary_currency = SuperjobRuSpider.salary_normalizer(vacancy_salary)
        #print(f'---------------------------\n{vacancy_name}\n{vacancy_url}\n{vacancy_salary}\n--------------------------')
        #print(f'---------------------------\n{vacancy_salary}\n--------------------------')
        #print(f'---------------------------\n{starts} до {ends} {salary_currency}\n--------------------------')
        # starts, ends, salary_currency = HhRuSpider.salary_normalizer(vacancy_salary)

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
        if 'от' in salary:
            tmp = (salary[2].replace('\xa0', ' ')).split(' ')
            starts = int(''.join(tmp[:2]))
            currency = tmp[2]
        if 'до' in salary:
            tmp = (salary[2].replace('\xa0', ' ')).split(' ')
            ends = int(''.join(tmp[:2]))
            currency = tmp[2]
        if '-' in salary:
            starts = int(salary[0].replace('\xa0', ''))
            ends = int(salary[4].replace('\xa0', ''))
            currency = salary[-3]
        #print(starts, ends, currency)
        return starts, ends, currency
