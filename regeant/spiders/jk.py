# -*- coding:utf-8 -*-


from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from regeant.models import RegeantItem, Producer, Brand
from .utils import HelperMixin


class JKCrawlerSpider(CrawlSpider, HelperMixin):
    name = "jk"
    allowed_domains = ['www.jkchemical.com']
    start_urls = [
        'http://www.jkchemical.com/SiteMap.aspx?language=ch'
        ]

    rules = (
        Rule(SgmlLinkExtractor(
            allow=('/CH/product/', )), callback='parse_item', follow=True),
        Rule(SgmlLinkExtractor(allow=()), follow=True)
    )

    def __init__(self):
        self.producer = Producer.objects.get(pk=2)
        self.brands = dict()

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        i = RegeantItem()
        i['product_name'] = self.join(
            hxs.select('//span[@id="ctl00_ContentPlaceHolder1_Label45"]/span[1]/text()').extract()) \
                if hxs.select('//span[@id="ctl00_ContentPlaceHolder1_Label45"]/span[1]/text()').extract() else ""
        i['product_english_name'] = self.join(
            hxs.select('//span[@id="ctl00_ContentPlaceHolder1_Label3"]/text()').extract()) \
                if hxs.select('//span[@id="ctl00_ContentPlaceHolder1_Label3"]/text()').extract() else ""
        i['product_no'] = self.join(
            hxs.select('//span[@id="ctl00_ContentPlaceHolder1_Label1"]/text()').extract()) \
                if hxs.select('//span[@id="ctl00_ContentPlaceHolder1_Label1"]/text()').extract() else ""
        i['cas_no'] = self.join(
            hxs.select('//a[@id="ctl00_ContentPlaceHolder1_HyperLink3"]/text()').extract()) \
                if hxs.select('//a[@id="ctl00_ContentPlaceHolder1_HyperLink3"]/text()').extract() else ""

        i['moleclar_structure_formation_path'] = self.join(
            hxs.select('//img[@id="ctl00_ContentPlaceHolder1_Image1"]/@src').extract()) \
                if hxs.select('//img[@id="ctl00_ContentPlaceHolder1_Image1"]/@src').extract() else ""
        i['description'] = self.join(
            hxs.select('//div[@id="ctl00_ContentPlaceHolder1_tbc_01"]/div[1]').extract()) \
                if hxs.select('//div[@id="ctl00_ContentPlaceHolder1_tbc_01"]/div[1]').extract() else ""
        i['producer'] = self.producer
        brand = self.join(
            hxs.select('//span[@id="ctl00_ContentPlaceHolder1_Label4"]/text()').extract()) \
             if hxs.select('//span[@id="ctl00_ContentPlaceHolder1_Label4"]/text()').extract() else ""

        if not brand in self.brands:
            new_brand = Brand()
            new_brand.name = brand
            new_brand.description = ' '.join((brand, "scraped from J&K"))
            new_brand.save()
            self.brands[brand, new_brand]
            i['brand'] = new_brand
        else:
            i['brand'] = self.brands[brand]

        i['url_path'] = response.url
        return i
