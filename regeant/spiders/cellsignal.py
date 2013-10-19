
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from regeant.models import RegeantItem, Producer, Brand
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