# -*- coding: utf-8 -*-


from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from regeant.models import RegeantItem, Producer, Brand
from .utils import HelperMixin


class ApplichemSpider(CrawlSpider, HelperMixin):
    name = 'applichem'
    allowed_domains = ['www.applichemus.com']
    start_urls = ['https://www.applichemus.com/products.php']

    rules = (
        Rule(SgmlLinkExtractor(
            allow=(r'/products.php', r'/products.php\?page=\d+')), follow=True),
        Rule(SgmlLinkExtractor(
            allow=(r'/[\w-]+\.html$',)), callback='parse_item'))

    def __init__(self):
        self.producer = Producer.objects.get(name='Applichem')
        self.brand = Brand.objects.get(name='Applichem')
        CrawlSpider.__init__(self)

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        i = RegeantItem()
        i['product_name'] = self.join(
            hxs.select('//div[@id="Content"]/div[2]/div[1]/div[1]/div/div/div/div[1]/div/table/tbody/tr[1]/td/text()').extract()) \
            if hxs.select('//div[@id="Content"]/div[2]/div[1]/div[1]/div/div/div/div[1]/div/table/tbody/tr[1]/td/text()').extract() else ""
        i['product_english_name'] = self.join(
            hxs.select('//div[@id="Content"]/div[2]/div[1]/div[1]/div/div/div/div[1]/div/table/tbody/tr[1]/td/text()').extract()) \
            if hxs.select('//div[@id="Content"]/div[2]/div[1]/div[1]/div/div/div/div[1]/div/table/tbody/tr[1]/td/text()').extract() else ""
        product_no = self.join(
            hxs.select('//div[@id="Content"]/div[2]/div[1]/div[1]/div/div/div/h1/span/text()').extract()) \
            if hxs.select('//div[@id="Content"]/div[2]/div[1]/div[1]/div/div/div/h1/span/text()').extract() else ""
        i['product_no'] = product_no.replace(u"Item#: ", u"")
        i['producer'] = self.producer
        i['brand'] = self.brand
        i['url_path'] = response.url
        return i
