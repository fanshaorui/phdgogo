from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from regeant.models import RegeantItem, Producer, Brand
from .utils import HelperMixin


class AnbobioSpider(CrawlSpider, HelperMixin):
    name = 'anbobio'
    allowed_domains = ['www.anbobio.com']
    start_urls = [
    #'http://www.anbobio.com/product_detail.asp?sort_id=65&shop_id=2657&page=1',
        'http://www.anbobio.com/products.asp'
    ]

    rules = (
        Rule(SgmlLinkExtractor(
            allow=('/product_detail', )), callback='parse_item'),
        Rule(SgmlLinkExtractor(allow=()), follow=True)
    )

    def __init__(self):
        self.producer = Producer.objects.get(name="Anbo Biotech")
        self.brand = Brand.objects.get(name="Anbo Biotech")
        CrawlSpider.__init__(self)

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        i = RegeantItem()
        i['product_name'] = ""
        product_english_name_sign = self.join(hxs.select('//div[@id="content"]/table[2]/tr[1]/td[@align="right"]/text()').extract())
        if product_english_name_sign == "Name:":
            i['product_english_name'] = self.join(hxs.select('//div[@id="content"]/table[2]/tr[1]/td[@align="left"]/text()').extract())
        else:
            i['product_english_name'] = ""
        i['cas_no'] = ""
        product_no_sign = self.join(hxs.select('//div[@id="content"]/table[2]/tr[3]/td[@align="right"]/text()').extract())
        if product_no_sign == "Catalog Number:":
            product_no = self.join(hxs.select('//div[@id="content"]/table[2]/tr[3]/td[@align="left"]/text()').extract())
        i['product_no'] = product_no
        i['description'] = self.join(hxs.select('//div[@id="content"]').extract()) \
                if hxs.select('//div[@id="content"]').extract() else ""
         
        path = hxs.select('//div[@id="content"]/table[2]/tr/td/img[1]/@src').extract() \
                if hxs.select('//div[@id="content"]/table[2]/tr/td/img[1]/@src').extract() else ""
        i['moleclar_structure_formation_path'] = "http://www.anbobio.com/"+path[0]
        i['producer'] = self.producer
        i['brand'] = self.brand
        i['url_path'] = response.url
        i['original_html'] = hxs.select('//td[@class="sku"]/p/text()').extract() 
        return i
