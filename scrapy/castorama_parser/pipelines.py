# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline

class CastoramaParserPipeline:
    def process_item(self, item, spider):
        return item

class CastoramaPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item.get('photos'):
            counter = 0
            for img in item.get('photos'):
                counter += 1
                img = f'https://castorama.ru{img}'
                try:
                    yield scrapy.Request(url=img, meta={'folder_name': item['name'], 'number': str(counter)})
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None, *, item=None):
        folder_name = request.meta['folder_name']
        number = request.meta['number']
        return f'/{folder_name}/{folder_name}_{number}.jpg'
        # return '/' + folder_name + '/' + folder_name + '_'+number

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item