# -*- coding: utf-8 -*-


from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from regeant.models import RegeantItem, Producer, Brand


class SigmaaldrichSpider(CrawlSpider):
	name = 'sigmaaldrich'
	allowed_domains = ['www.sigmaaldrich.com']
	start_urls = [
		'http://www.sigmaaldrich.com/china-mainland/zh/site-level/site-map.html'
		]

	rules =(
		Rule(SgmlLinkExtractor(
			allow=('/catalog/product/', )), callback='parse_item'),
		Rule(SgmlLinkExtractor(allow=()), follow=True)
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
			product_no = ''.join(product_no.replace(u'产品编号',u'').replace(u'|',u'').split())
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

	def join(self, group):
		if len(group) > 0:
			return ''.join(group).strip()
		else:
			return ""


class CaymanSpider(CrawlSpider):
	name = 'cayman'
	allowed_domains = ['www.caymanchem.com']
	start_urls = [
	#'https://www.caymanchem.com/app/template/Product.vm/catalog/14100',
		'https://www.caymanchem.com/app/template/productQualifiers%2CHome.vm'
	]

	rules =(
		Rule(SgmlLinkExtractor(
			allow=('/app/template/Product.vm/catalog/', )), callback='parse_item'),
		Rule(SgmlLinkExtractor(allow=()), follow=True)
	)
	def __init__(self):
		self.producer = Producer.objects.get(name="Cayman")
		self.brand = Brand.objects.get(name="Cayman")
		CrawlSpider.__init__(self)
	def join(self, group):
		if len(group) > 0:
			return ''.join(group).strip()
		else:
			return ""
	def parse_item(self, response):
		hxs = HtmlXPathSelector(response)
		i = RegeantItem()
		i['product_name'] = ""
		i['product_english_name'] = self.join(hxs.select('//h1/span[@class="scientificMarkup"]/text()').extract())
		cas_title=self.join(hxs.select('//table[@id="data"]/tr[3]/th/text()').extract())
		if cas_title=="CAS Number":
			i['cas_no']=self.join(hxs.select('//table[@id="data"]/tr[3]/td/text()').extract())
		else:
			i['cas_no']=""
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
class CellsignalSpider(CrawlSpider):
	name = 'cellsignal'
	allowed_domains = ['www.cellsignal.com']
	start_urls = [
	#'http://www.cellsignal.com/products/12046.html',
		'http://www.cellsignal.com/catalog/index.html'
	]

	rules =(
		Rule(SgmlLinkExtractor(
			allow=('/products/', )), callback='parse_item'),
		Rule(SgmlLinkExtractor(allow=()), follow=True)
	)
	def __init__(self):
		self.producer = Producer.objects.get(name="CST")
		self.brand = Brand.objects.get(name="CST")
		CrawlSpider.__init__(self)
	def join(self, group):
		if len(group) > 0:
			return ''.join(group).strip()
		else:
			return ""
	def parse_item(self, response):
		hxs = HtmlXPathSelector(response)
		i = RegeantItem()
		i['product_name'] = ""
		product_english_name=self.join(hxs.select('//h1[@class="productName"]/text()').extract())
		s=product_english_name.find("#")
		i['product_english_name'] = product_english_name[0:s]
		i['cas_no']=""
		product_no = response.url
		if product_no:
			product_no=product_no.encode("gbk")
			product_no = filter(str.isdigit,product_no)
		i['product_no'] = product_no
		i['description'] = self.join(hxs.select('//div[@id="background"]/p/text()').extract()) \
				if hxs.select('//div[@id="background"]/p/text()').extract() else ""
		i['moleclar_structure_formation_path'] = self.join(
			hxs.select('//div[@id="product-images"]/div[1]/a/@href').extract()) \
				if hxs.select('//div[@id="product-images"]/div[1]/a/@href').extract() else ""
		i['producer'] = self.producer
		i['brand'] = self.brand
		i['url_path'] = response.url
		i['original_html'] = response.body.strip()
		return i
class AnbobioSpider(CrawlSpider):
	name = 'anbobio'
	allowed_domains = ['www.anbobio.com']
	start_urls = [
	#'http://www.anbobio.com/product_detail.asp?sort_id=65&shop_id=2657&page=1',
		'http://www.anbobio.com/products.asp'
	]

	rules =(
		Rule(SgmlLinkExtractor(
			allow=('/product_detail', )), callback='parse_item'),
		Rule(SgmlLinkExtractor(allow=()), follow=True)
	)
	def __init__(self):
		self.producer = Producer.objects.get(name="Anbo Biotech")
		self.brand = Brand.objects.get(name="Anbo Biotech")
		CrawlSpider.__init__(self)
	def join(self, group):
		if len(group) > 0:
			return ''.join(group).strip()
		else:
			return ""
	def parse_item(self, response):
		hxs = HtmlXPathSelector(response)
		i = RegeantItem()
		i['product_name'] = ""
		product_english_name_sign=self.join(hxs.select('//div[@id="content"]/table[2]/tr[1]/td[@align="right"]/text()').extract())
		if product_english_name_sign=="Name:":
			i['product_english_name'] = self.join(hxs.select('//div[@id="content"]/table[2]/tr[1]/td[@align="left"]/text()').extract())
		else:
			i['product_english_name']=""
		i['cas_no']=""
		product_no_sign=self.join(hxs.select('//div[@id="content"]/table[2]/tr[3]/td[@align="right"]/text()').extract())
		if product_no_sign=="Catalog Number:":
			product_no = self.join(hxs.select('//div[@id="content"]/table[2]/tr[3]/td[@align="left"]/text()').extract())
		i['product_no'] = product_no
		i['description'] = self.join(hxs.select('//div[@id="content"]').extract()) \
				if hxs.select('//div[@id="content"]').extract() else ""
		 
		path=hxs.select('//div[@id="content"]/table[2]/tr/td/img[1]/@src').extract() \
				if hxs.select('//div[@id="content"]/table[2]/tr/td/img[1]/@src').extract() else ""
		print path
		i['moleclar_structure_formation_path'] ="http://www.anbobio.com/"+path[0]
		i['producer'] = self.producer
		i['brand'] = self.brand
		i['url_path'] = response.url
		i['original_html'] = response.body.strip()
		return i
class AmeriscoSpider(CrawlSpider):
	name = 'amerisco'
	allowed_domains = ['www.amresco-inc.com']
	start_urls = [
	#'http://www.amresco-inc.com/rna-loading-buffer-with-etbr-1b1607.cmsx',
		'http://www.amresco-inc.com/home/products/products-home.cmsx'
	]

	rules =(
		Rule(SgmlLinkExtractor(
			allow=('/home/', ),deny=('.pdf', )),follow=True),
		Rule(SgmlLinkExtractor(allow=()), callback='parse_item',follow=True)
	)
	def __init__(self):
		self.producer = Producer.objects.get(name="AMRESCO")
		self.brand = Brand.objects.get(name="AMRESCO")
		CrawlSpider.__init__(self)
	def join(self, group):
		if len(group) > 0:
			return ''.join(group).strip()
		else:
			return ""
	def parse_item(self, response):
		hxs = HtmlXPathSelector(response)
		i = RegeantItem()
		#因为该网站产品名为简写,故而在中文名处填入其英文完整名称
		i['product_name'] = hxs.select('//div[@id="topleft"]/dl[2]/dd[1]/text()').extract()
		i['product_english_name']=hxs.select('//h1/text()').extract()[1]
		cas_no_sign=hxs.select('//div[@id="topleft"]/dl[1]/dt[1]/text()').extract()
		if cas_no_sign=="CAS Number: ":
			i['cas_no']=hxs.select('//div[@id="topleft"]/dl[1]/dd[1]/text()').extract()
		else:
			i['cas_no']=""
		i['product_no'] = hxs.select('//h1/text()').extract()[0]
		i['description'] = self.join(hxs.select('//div[@id="product_description"]').extract()) \
				if hxs.select('//div[@id="product_description"]').extract() else ""
		 
		i['moleclar_structure_formation_path'] =""
		i['producer'] = self.producer
		i['brand'] = self.brand
		i['url_path'] = response.url
		i['original_html'] = response.body.strip()
		return i
