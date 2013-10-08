# -*- coding: utf-8 -*-


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.exceptions import DropItem


class SigmaPipeline(object):

    def __init__(self):
        self.crawled = set()
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute(
            r"SELECT `product_no`,`producer_id` FROM `regeant_regeant`")

        for item in cursor.fetchall():
            self.crawled.add((item[0], item[1]))

    def process_item(self, item, spider):
        crawled_tuple = (item['product_no'], item['producer'].id)
        if not crawled_tuple in self.crawled:
            item.save()
            self.crawled.add(crawled_tuple)
            return item
        else:
            raise DropItem("Drop repeated record.")
