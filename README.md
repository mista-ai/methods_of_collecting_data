# job_parser

Job_parser is a Python script for scraping hh.ru

## Installation

Use the package manager [pip] to install scrapy.

```
pip install scrapy
```

## Usage
If you want to scrapy certain vacancy go to self.start_urls in "spiders/hh_ru.py" and add url of hh.ru with job name, which you want to parse.
```python
class HhRuSpider(scrapy.Spider):
    name = "hh_ru"
    allowed_domains = ["hh.ru"]
    start_urls = ["http://hh.ru/"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = []
```

## Structure
This project is made with scrapy template. So the structure is next:

Spiders are in 'spiders' folder.  
Settings of parser are in 'settings'  
In items we transmit and process our parsed items  
And in pipelines we process data again. For example here we save our items in mongodb

``` python
class JobParserPipeline:
    def __init__(self):
        super().__init__()
        client = MongoClient('localhost:27017')
        self.mongo_db = client.jobs_parser

    def process_item(self, item, spider):
        collection = self.mongo_db[spider.name]
        collection.insert_one(item)
        return item
```

The database structure is next:
hh_ru collection in jobs_parser db.  
Each hh_ru element(vacancy) has name(str), salary_from(int), salary_to(int), currency(str), compensation_type(str), company(str), key_skills(array) and _id

You can see examples of requests in mongo requests.ipynb
