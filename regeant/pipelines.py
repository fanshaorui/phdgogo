# -*- coding: utf-8 -*-


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.exceptions import DropItem


class ItemPipeline(object):

    def __init__(self):
        self.crawled_init = False
        self.crawled = set()

    def process_item(self, item, spider):
        self.init_crawled(spider)
        crawled_tuple = (item['product_no'], item['producer'].id)
        if not crawled_tuple in self.crawled:
            item.save()
            self.crawled.add(crawled_tuple)
            return item
        else:
            raise DropItem("Drop repeated record.")

    def init_crawled(self, spider):
        if not self.crawled_init:
            from django.db import connection
            cursor = connection.cursor()
            cursor.execute(
                r"SELECT `product_no`,`producer_id` FROM `regeant_regeant` \
                    WHERE `producer_id`=%s", (spider.producer.id,))

            for item in cursor.fetchall():
                self.crawled.add((item[0], item[1]))

            self.crawled_init = True
