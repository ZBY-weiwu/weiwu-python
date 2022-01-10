# Scrapy settings for lihkg project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'lihkg_search'

SPIDER_MODULES = ['lihkg_search.spiders']
NEWSPIDER_MODULE = 'lihkg_search.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'lihkg (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

CONCURRENT_REQUESTS = 1
RETRY_ENABLED = False
DOWNLOAD_TIMEOUT = 5
# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 8
CONCURRENT_REQUESTS_PER_IP = 8

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'lihkg_search.middlewares.proxMiddleware': 543,
#    'lihkg_search.middlewares.RotateUserAgentMiddleware':400,
#    #'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware':None,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware':None,
    'lihkg_search.middlewares.RotateUserAgentMiddleware':400,
    'lihkg_search.middlewares.MyproxiesSpiderMiddleware':125
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    #'lihkg_search.pipelines.LihkgPipeline': 300,
    #'lihkg_search.pipelines.Lihkg_reply': 300
    'lihkg_search.pipelines.ElasticsearchPipeline' :400,
    'lihkg_search.pipelines.ElasticsearchPipeline_Reply' :450,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

#IPPOOL=[{"ipaddr":"http://192.168.1.10:1081"}]
IPPOOL=[{'http': 'http://192.168.1.44:1081', 'https': 'https://192.168.1.44:1081'},
                {'http': 'http://192.168.1.49:1081', 'https': 'https://192.168.1.49:1081'},
                {'http': 'http://192.168.1.50:1081', 'https': 'https://192.168.1.50:1081'},
                {'http': 'http://192.168.1.51:1081', 'https': 'https://192.168.1.51:1081'},
                {'http': 'http://192.168.1.52:1081', 'https': 'https://192.168.1.52:1081'},
                {'http': 'http://192.168.1.53:1081', 'https': 'https://192.168.1.53:1081'},
                {'http': 'http://192.168.1.54:1081', 'https': 'https://192.168.1.54:1081'},
                {'http': 'http://192.168.1.55:1081', 'https': 'https://192.168.1.55:1081'},
                {'http': 'http://192.168.1.56:1081', 'https': 'https://192.168.1.56:1081'},
                {'http': 'http://192.168.1.57:1081', 'https': 'https://192.168.1.57:1081'}]

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
LOG_LEVEL='INFO'
