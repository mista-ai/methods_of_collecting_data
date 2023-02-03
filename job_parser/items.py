# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Compose
from twisted.web.html import output


# def process_salary(salary):
#     starts = None
#     ends = None
#     currency = None
#     compensation_type = None
#     if 'от ' in salary:
#         starts = salary[1].replace('\xa0', '')
#         starts = int(starts)
#     if 'до ' in salary:
#         ends = salary[1].replace('\xa0', '')
#         ends = int(ends)
#     if ' до ' in salary:
#         ends = salary[3].replace('\xa0', '')
#         ends = int(ends)
#     if len(salary) > 1:
#         currency = salary[-3]
#         compensation_type = salary[-1]
#     return {'from': starts, 'to': ends, 'currency': currency, 'compensation-type': compensation_type}


def process_company(company):
    length = len(company) // 2
    company = company[:length]
    company = (' '.join(company)).replace('\xa0', '')
    print(company, type(company))
    if not company:
        return '-'
    return company


class JobParserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    # salary = scrapy.Field(input_processor=Compose(process_salary), output_processor=TakeFirst())
    salary_from = scrapy.Field(output_processor=TakeFirst())
    salary_to = scrapy.Field(output_processor=TakeFirst())
    currency = scrapy.Field(output_processor=TakeFirst())
    compensation_type = scrapy.Field(output_processor=TakeFirst())
    company = scrapy.Field(input_processor=Compose(process_company), output_processor=TakeFirst())
    key_skills = scrapy.Field()
    _id = scrapy.Field()
    print()
