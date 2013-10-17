# -*- coding: utf-8 -*-


from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from regeant.models import RegeantItem, Producer, Brand


def join(group):

    '''simple join function to process crawled nodes.'''

    if len(group) > 0:
        return ''.join(group).strip()
    else:
        return ""


class AladdinSpider(CrawlSpider):
    name = 'aladdin'
    allowed_domains = ['www.aladdin-e.com']
    start_urls = [
        'http://www.aladdin-e.com/service/site_map.jsp'
        ]

    rules =(
        Rule(SgmlLinkExtractor(
            allow=(r'/itemDetail.do?cust_item=(\w+)&whs_id=1',)), callback='parse_item'),
        Rule(SgmlLinkExtractor(allow=()), follow=True)
    )

    def __init__(self):
        self.producer = Producer.objects.get(pk=2)
        self.brand = Brand.objects.get(pk=2)
        CrawlSpider.__init__(self)

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        i = RegeantItem()
        i['product_name'] = join(
            hxs.select('//div[contains(@class,"itmdetMainPanel")]/div[1]/div[2]/h1/text()').extract()) \
                if hxs.select('//div[contains(@class,"itmdetMainPanel")]/div[1]/div[2]/h1/text()').extract() else ""
        product_eng_name = join(
            hxs.select('//div[contains(@class, "itmdetMainPanel")]/div[2]/div[1]/div[1]/span/text()').extract()) \
                if hxs.select('//div[contains(@class, "itmdetMainPanel")]/div[2]/div[1]/div[1]/span/text()').extract() else ""
        product_eng_name = product_eng_name.replace("Product Name: ", "")
        i['product_english_name'] = product_eng_name
        i['product_no'] = join(
            hxs.select(
                '//div[contains(@class,"itmdetMainPanel")]/div[1]/div[1]/h1[@class="itmdet-topbar-itmnum"]/text()').extract()) \
                    if hxs.select('//div[contains(@class,"itmdetMainPanel")]/div[1]/div[1]/h1[@class="itmdet-topbar-itmnum"]/text()').extract() else None
        i['cas_no'] = join(
            hxs.select('//table[@class="productOverViewInfo"]/tbody/tr[2]/td[2]/a/text()').extract()) \
                if hxs.select('//table[@class="productOverViewInfo"]/tbody/tr[2]/td[2]/a/text()').extract() else ""
        
        i['moleclar_structure_formation_path'] = "http://www.aladdin-e.com" + join(
            hxs.select('//div[@id="album"]/a/img/@src').extract()) \
                if hxs.select('//div[@id="album"]/a/img/@src').extract() else ""
        i['description'] = join(
            hxs.select('//div[@id="itemDetailTab"]/div[2]/div[1]/div/table').extract()) \
                if hxs.select('//div[@id="itemDetailTab"]/div[2]/div[1]/div/table').extract() else ""
        i['molecular_equation'] = join(
            hxs.select('string(//tr[@id="itmdet-baseCnt-formula"]/td[2])').extract()) \
                if hxs.select('string(//tr[@id="itmdet-baseCnt-formula"]/td[2])').extract() else ""
        i['molecular_weight'] = float(join(
            hxs.select('//table[@class="productOverViewInfo"]/tbody/tr[4]/td[2]/text()').extract())) \
                if hxs.select('//table[@class="productOverViewInfo"]/tbody/tr[4]/td[2]/text()').extract() else 0
        i['producer'] = self.producer
        i['brand'] = self.brand
        i['url_path'] = response.url
        return i
