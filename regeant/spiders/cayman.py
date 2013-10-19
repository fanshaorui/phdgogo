from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from regeant.models import RegeantItem, Producer, Brand
from .utils import HelperMixin


class CaymanSpider(CrawlSpider, HelperMixin):
    name = 'cayman'
    allowed_domains = ['www.caymanchem.com']
    start_urls = [
        'https://www.caymanchem.com/app/template/productQualifiers%2CHome.vm'
    ]

    rules = (
        Rule(SgmlLinkExtractor(
            allow=('/app/template/Product.vm/catalog/', )), callback='parse_item'),
        Rule(SgmlLinkExtractor(allow=()), follow=True)
    )

    def __init__(self):
        self.producer = Producer.objects.get(name="Cayman")
        self.brand = Brand.objects.get(name="Cayman")
        CrawlSpider.__init__(self)

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        i = RegeantItem()
        i['product_name'] = ""
        i['product_english_name'] = self.join(hxs.select('//h1/span[@class="scientificMarkup"]/text()').extract())
        cas_title = self.join(hxs.select('//table[@id="data"]/tr[3]/th/text()').extract())
        if cas_title == "CAS Number":
            i['cas_no'] = self.join(hxs.select('//table[@id="data"]/tr[3]/td/text()').extract())
        else:
            i['cas_no'] = ""
        product_no = self.join(hxs.select('//p[@class="catalogNumber"]/text()').extract()) \
                if hxs.select('//p[@class="catalogNumber"]/text()').extract() else None
        if product_no:
            product_no=product_no.encode("gbk")
            product_no = filter(str.isdigit,product_no)
        i['product_no'] = product_no
        i['description'] = self.join(hxs.select('//div[@id="description"]').extract()) \
                if hxs.select('//div[@id="description"]').extract() else ""
        i['moleclar_structure_formation_path'] = self.join(
            hxs.select('//img[@id="productImage"]/@src').extract()) \
                if hxs.select('//img[@id="productImage"]/@src').extract() else ""
        i['producer'] = self.producer
        i['brand'] = self.brand
        i['url_path'] = response.url
        i['original_html'] = response.body.strip()
        return i
