# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter
import pandas as pd


class BizwirePipeline:
    def process_item(self, item, spider):
        return item

class CsvPipeline(object):
    def __init__(self):
        self.file = open('kaist_bizwire.csv', 'wb')
        self.exporter = CsvItemExporter(self.file, encoding='utf-8')
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
        df = pd.read_csv('kaist_bizwire.csv')
        excel = pd.ExcelWriter('kaist_bizwire.xlsx')
        df.to_excel(excel, index = False)
        excel.save()


    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item