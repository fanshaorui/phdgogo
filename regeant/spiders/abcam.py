# -*- coding: utf-8 -*-


from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from regeant.models import RegeantItem, Producer, Brand
from .utils import HelperMixin


class AbcamSpider(CrawlSpider, HelperMixin):
    name = 'abcam'
    allowed_domains = ['www.abcam.cn']
    start_urls = [
        'http://www.abcam.cn/index.html?pageconfig=productmap&cl=2282',
        'http://www.abcam.cn/index.html?pageconfig=productmap&cl=253',
        'http://www.abcam.cn/index.html?pageconfig=productmap&cl=246',
        'http://www.abcam.cn/index.html?pageconfig=productmap&cl=4588',
        'http://www.abcam.cn/index.html?pageconfig=productmap&cl=250',
        'http://www.abcam.cn/index.html?pageconfig=productmap&cl=249',
        'http://www.abcam.cn/index.html?pageconfig=productmap&cl=252',
        'http://www.abcam.cn/index.html?pageconfig=productmap&cl=248',
        'http://www.abcam.cn/index.html?pageconfig=productmap&cl=2105',
        'http://www.abcam.cn/index.html?pageconfig=productmap&cl=3427']

    rules = (
        Rule(SgmlLinkExtractor(
            allow=(r'/products\?selected.researchAreas=[\w-+]+&selected.productType=[\w-+]+',)), follow=True),
        Rule(SgmlLinkExtractor(
            allow=(r'/[\w-]+\.html$',)), callback='parse_item'),)

    def __init__(self):
        self.producer = Producer.objects.get(name='Abcam')
        self.brand = Brand.objects.get(name='Abcam')
        CrawlSpider.__init__(self)

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        i = RegeantItem()
        i['product_name'] = self.join(
            hxs.select('//div[@id="datasheet-header-container"]/div[1]/div[1]/div[1]/h1/text()').extract()) \
            if hxs.select('//div[@id="datasheet-header-container"]/div[1]/div[1]/div[1]/h1/text()').extract() else ""
        i['product_english_name'] = self.join(
            hxs.select('//div[@id="datasheet-header-container"]/div[1]/div[1]/div[1]/h1/text()').extract()) \
            if hxs.select('//div[@id="datasheet-header-container"]/div[1]/div[1]/div[1]/h1/text()').extract() else ""
        product_no = self.join(
            hxs.select('//div[@id="size-information"]/div/div[1]/h3/text()').extract()) \
            if hxs.select('//div[@id="size-information"]/div/div[1]/h3/text()').extract() else ""
        i['product_no'] = product_no.replace(u"Product code ", u"")
        i['description'] = self.join(
            hxs.select('//div[@id="tabs"]/div[4]').extract()) \
            if hxs.select('//div[@id="tabs"]/div[4]').extract() else ""
        i['producer'] = self.producer
        i['brand'] = self.brand
        i['url_path'] = response.url
        return i
