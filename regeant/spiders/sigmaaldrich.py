# -*- coding: utf-8 -*-


from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from regeant.models import RegeantItem, Producer, Brand
from .utils import HelperMixin


class SigmaaldrichSpider(CrawlSpider, HelperMixin):
    name = 'sigmaaldrich'
    allowed_domains = ['www.sigmaaldrich.com']
    start_urls = [
        'http://www.sigmaaldrich.com/china-mainland/zh/life-science.html',
        'http://www.sigmaaldrich.com/china-mainland/zh/analytical-chromatography.html',
        'http://www.sigmaaldrich.com/china-mainland/zh/chemistry.html',
        'http://www.sigmaaldrich.com/china-mainland/zh/materials-science.html',
        'http://www.sigmaaldrich.com/china-mainland/zh/labware.html',
        'http://www.sigmaaldrich.com/content/safc-global.html',
        ]

    rules = (
        Rule(SgmlLinkExtractor(
            allow=(r'/catalog/product/', ), deny=(r'search')), callback='parse_item'),
        Rule(SgmlLinkExtractor(allow=(), deny=(r'search')), follow=True)
    )

    def __init__(self):
        self.producer = Producer.objects.get(pk=1)
        self.brand = Brand.objects.get(pk=1)
        CrawlSpider.__init__(self)

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        i = RegeantItem()
        i['product_name'] = self.join(
            hxs.select('string(//h1[@itemprop="name"])').extract()) \
            if hxs.select('string(//h1[@itemprop="name"])').extract() else ""
        i['product_english_name'] = self.join(
            hxs.select('string(//h2[@class="english_subtitle"])').extract()) \
            if hxs.select('//h2[@class="english_subtitle"]/text()').extract() else ""
        product_no = self.join(
            hxs.select('//strong[@itemprop="productID"]/text()').extract()) \
            if hxs.select('//strong[@itemprop="productID"]/text()').extract() else None
        if product_no:
            product_no = ''.join(product_no.replace(u'产品编号', u'').replace(u'|', u'').split())
        i['product_no'] = product_no
        cas_tag = ''.join(
            hxs.select('//div[@id="productDetailHero"]/div/div[1]/strong[2]/text()').extract()[0].split())
        if cas_tag == u'CAS号':
            i['cas_no'] = self.join(
                hxs.select('//div[@class="productInfo twoThirds"]/strong/a/text()').extract()) \
                if hxs.select('//div[@class="productInfo twoThirds"]/strong/a/text()').extract() else ""

        i['moleclar_structure_formation_path'] = "http://www.sigmaaldrich.com" + self.join(
            hxs.select('//div[contains(@class,"prodImage")]/a/img/@src').extract()) \
            if hxs.select('//div[contains(@class,"prodImage")]/a/img/@src').extract() else ""
        i['description'] = self.join(
            hxs.select('//div[@id="productDetailProperties"]').extract()) \
            if hxs.select('//div[@id="productDetailProperties"]').extract() else ""
        i['wiki'] = self.join(
            hxs.select('id("productDetailProtocols")/child::div').extract()) \
            if hxs.select('id("productDetailProtocols")/child::div').extract() else ""
        i['references'] = self.join(
            hxs.select('//div[contains(@class, "detailRightColumn")]/p/a').extract()) \
            if hxs.select('//div[contains(@class, "detailRightColumn")]/p/a').extract() else ""
        i['producer'] = self.producer
        i['brand'] = self.brand
        i['url_path'] = response.url
        i['original_html'] = response.body.strip()
        return i

    def parse_start_url(self, response):
        if not hasattr(response, 'encoding'):
            setattr(response, 'encoding', 'text/html;charset=UTF-8')
        target_le = SgmlLinkExtractor(
            allow='/catalog/product/')
        links = target_le.extract_links(response)
        if links:
            return [Request(url=link.url, cookies = dict(country="CHIM",
            SialLocaleDef="CountryCode~CN|WebLang~-7|",
            SessionPersistence="""CLICKSTREAMCLOUD%3A%3DvisitorId%3Danonymous%7CPROFILEDATA%3A%3D
            avatar%3D%2Fetc%2Fdesigns%2Fdefault%2Fimages%2Fcollab%2Favatar.png%2CauthorizableId%3D
            anonymous%2CauthorizableId_xss%3Danonymous%2CformattedName%3D%2CformattedName_xss%3D%7C
            SURFERINFO%3A%3DIP%3D141.247.239.190%2Ckeywords%3D%2Cbrowser%3DUnresolved%2COS%3DMac%20OS
            %20X%2Cresolution%3D1440x900%7C""", 
            GUID="415dfb24-e4f2-4218-a5d7-b2943d012103|NULL|1380870456876", 
            cmTPSet="Y"), callback=self.parse_item) 
                for link in links]
        else:
            general_le = SgmlLinkExtractor(
                        allow=())
            return [Request(url=link.url, cookies = dict(country="CHIM", 
                SialLocaleDef="CountryCode~CN|WebLang~-7|", 
                SessionPersistence="""CLICKSTREAMCLOUD%3A%3DvisitorId%3Danonymous%7CPROFILEDATA%3A%3D
                avatar%3D%2Fetc%2Fdesigns%2Fdefault%2Fimages%2Fcollab%2Favatar.png%2CauthorizableId%3D
                anonymous%2CauthorizableId_xss%3Danonymous%2CformattedName%3D%2CformattedName_xss%3D%7C
                SURFERINFO%3A%3DIP%3D141.247.239.190%2Ckeywords%3D%2Cbrowser%3DUnresolved%2COS%3DMac%20OS
                %20X%2Cresolution%3D1440x900%7C""", 
                GUID="415dfb24-e4f2-4218-a5d7-b2943d012103|NULL|1380870456876", 
                cmTPSet="Y"))
                    for link in general_le.extract_links(response)]
