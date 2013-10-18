# Scrapy settings for crawlers project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "search_demo.settings")

BOT_NAME = 'crawlers'

SPIDER_MODULES = ['regeant.spiders']
NEWSPIDER_MODULE = 'regeant.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'crawlers (+http://www.yourdomain.com)'
# user-agent
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:24.0) Gecko/20100101 Firefox/24.0'
# request headers
DEFAULT_REQUEST_HEADERS = {
	'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3'
}
COOKIES_ENABLED = True

# Pipeline
ITEM_PIPELINES = [
    'regeant.pipelines.ItemPipeline',
]

DNSCACHE_ENABLED = True

DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleFifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.FifoMemoryQueue'

# Auto throttle
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5.0
AUTOTHROTTLE_MAX_DELAY = 120.0
