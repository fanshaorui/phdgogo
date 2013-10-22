# -*- coding: utf-8 -*-


from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from regeant.models import RegeantItem, Producer, Brand
from .utils import HelperMixin


class AbnovaSpider(CrawlSpider, HelperMixin):
    name = 'abnova'
    allowed_domains = ['www.abnova.com']
    start_urls = ['http://www.abnova.com/products/index.asp?SL=CN']

    rules = (
        Rule(SgmlLinkExtractor(
            allow=(r'/cn/products/products_list.asp\?classid=\w+&OwnClass=\d',)), follow=True),
        Rule(SgmlLinkExtractor(
            allow=(r'/cn/products/products_detail.asp\?Catalog_id=\w+',)), callback='parse_item'),)

    def __init__(self):
        self.producer = Producer.objects.get(name='Abnova')
        self.brand = Brand.objects.get(name='Abnova')
        self.forged_cookie = dict(CookiesAbnovaSelectLanguage="CN")
        CrawlSpider.__init__(self)

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        i = RegeantItem()
        i['product_name'] = self.join(
            hxs.select('//div[@id="table_section"]/h1/b/text()').extract()) \
            if hxs.select('//div[@id="table_section"]/h1/b/text()').extract() else ""
        i['product_english_name'] = self.join(
            hxs.select('//div[@id="table_section"]/h1/b/text()').extract()) \
            if hxs.select('//div[@id="table_section"]/h1/b/text()').extract() else ""
        product_no = self.join(
            hxs.select('//div[@id="catid_country"]/ul/li[1]/text()').extract()) \
            if hxs.select('//div[@id="catid_country"]/ul/li[1]/text()').extract() else ""
        i['product_no'] = self.join(product_no.replace(u"目录号 # : ", u""))
        i['scale_ext1'] = self.join(
            hxs.select('//div[@id="price_info"]/ul[2]/li[1]/text()').extract()) \
            if hxs.select('//div[@id="price_info"]/ul[2]/li[1]/text()').extract() else ""
        i['ext_attr1'] = self.join(self.join(
            hxs.select('//div[@id="price_info"]/ul[2]/li[2]/text()').extract())) \
            if hxs.select('//div[@id="price_info"]/ul[2]/li[2]/text()').extract() else ""
        i['description'] = self.join(
            hxs.select('//div[@id="datalist"]').extract()) \
            if hxs.select('//div[@id="datalist"]').extract() else ""
        i['producer'] = self.producer
        i['brand'] = self.brand
        i['url_path'] = response.url
        return i

    def parse_start_url(self, response):
        if not hasattr(response, 'encoding'):
            setattr(response, 'encoding', 'text/html;charset=UTF-8')
        target_le = SgmlLinkExtractor(
            allow=r'/cn/products/products_detail.asp\?Catalog_id=\w+')
        links = target_le.extract_links(response)
        if links:
            return [Request(url=link.url, cookies=self.forged_cookie, callback=self.parse_item) 
                for link in links]
        else:
            general_le = SgmlLinkExtractor(
                        allow=())
            return [Request(url=link.url, cookies=self.forged_cookie)
                    for link in general_le.extract_links(response)]

