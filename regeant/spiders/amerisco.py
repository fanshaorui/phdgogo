from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from regeant.models import RegeantItem, Producer, Brand
from .utils import HelperMixin


class AmeriscoSpider(CrawlSpider, HelperMixin):
    name = 'amerisco'
    allowed_domains = ['www.amresco-inc.com']
    start_urls = [
    #'http://www.amresco-inc.com/rna-loading-buffer-with-etbr-1b1607.cmsx',
        'http://www.amresco-inc.com/home/products/products-home.cmsx'
    ]

    rules = (
        Rule(SgmlLinkExtractor(
            allow=('/home/', ),deny=('.pdf', )),follow=True),
        Rule(SgmlLinkExtractor(allow=()), callback='parse_item',follow=True)
    )

    def __init__(self):
        self.producer = Producer.objects.get(name="AMRESCO")
        self.brand = Brand.objects.get(name="AMRESCO")
        CrawlSpider.__init__(self)

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        i = RegeantItem()
        i['product_name'] = hxs.select('//div[@id="topleft"]/dl[2]/dd[1]/text()').extract()
        i['product_english_name'] = hxs.select('//h1/text()').extract()[1]
        cas_no_sign = hxs.select('//div[@id="topleft"]/dl[1]/dt[1]/text()').extract()
        if cas_no_sign == "CAS Number: ":
            i['cas_no'] = hxs.select('//div[@id="topleft"]/dl[1]/dd[1]/text()').extract()
        else:
            i['cas_no'] = ""
        i['product_no'] = hxs.select('//h1/text()').extract()[0]
        i['description'] = self.join(hxs.select('//div[@id="product_description"]').extract()) \
                if hxs.select('//div[@id="product_description"]').extract() else ""

        i['moleclar_structure_formation_path'] = ""
        i['producer'] = self.producer
        i['brand'] = self.brand
        i['url_path'] = response.url
        i['original_html'] = response.body.strip()
        return i
