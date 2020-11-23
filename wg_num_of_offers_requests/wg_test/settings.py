# Scrapy settings for wg_test project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'wg_test'

SPIDER_MODULES = ['wg_test.spiders']
NEWSPIDER_MODULE = 'wg_test.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 10

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

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
#    'wg_test.middlewares.WgTestSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#     'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
# }

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 400,
}

# ROTATING_PROXY_LIST = [
#     'https://37.203.17.195:53281',
# 'https://139.59.122.123:1080',
# 'https://212.237.58.208:8080',
# 'https://80.211.14.207:53',
# 'https://194.182.74.160:3128',
# 'https://178.210.29.125:53281',
# 'https://194.182.74.151:3128',
# 'https://13.115.228.99:3128',
# 'https://38.96.9.236:8008',
# 'https://194.182.74.206:3128',
# 'https://89.236.17.106:3128',
# 'https://194.182.74.163:3128',
# 'https://188.213.171.41:8080',
# 'https://13.57.207.226:3128',
# 'https://194.182.74.248:3128',
# 'https://194.182.74.203:3128',
# 'https://35.196.89.215:80',
# 'https://194.182.74.110:3128',
# 'https://52.164.249.198:3128',
# 'https://194.182.74.51:3128',
# 'https://159.65.0.210:3128',
# 'https://195.49.200.154:8080',
# 'https://147.135.210.114:54566',
# 'https://59.106.215.9:3128',
# 'https://185.93.3.123:8080',
# 'https://160.16.127.184:3128',
# 'https://144.217.204.254:3128',
# 'https://92.222.79.39:8181',
# 'https://51.15.86.88:3128',
# 'https://151.80.140.233:54566',
# 'https://194.182.74.168:3128',
# 'https://5.196.169.98:3128',
# 'https://110.77.194.74:42619',
# 'https://200.95.174.132:3128',
# 'https://41.0.237.195:8080',
# 'https://104.46.34.250:3128',
# 'https://203.126.218.186:80',
# 'https://153.149.169.207:3128',
# 'https://153.149.170.147:3128',
# 'https://64.52.84.2:3128',
# 'https://47.206.51.67:8080',
# 'https://82.83.200.84:8080',
# 'https://5.197.183.222:8080',
# 'https://51.15.227.220:3128',
# 'https://187.188.168.51:52335',
# 'https://37.29.82.115:65103',
# 'https://92.53.73.138:8118',
# 'https://190.11.32.94:53281',
# 'https://194.126.183.141:53281',
# 'https://46.250.28.189:53281',
# 'https://187.44.83.227:3128',
# 'https://5.189.146.57:80',
# 'https://153.149.170.11:3128',
# 'https://177.204.85.203:80',
# 'https://185.52.76.103:8080',
# 'https://93.174.92.177:443',
# 'https://213.6.40.142:80',
# 'https://145.249.106.107:8118',
# 'https://202.93.128.98:3128',
# 'https://13.251.42.245:8080',
# 'https://128.199.198.79:8118',
# 'https://96.85.167.5:3128',
# 'https://194.246.105.52:53281',
# 'https://181.196.50.238:65103',
# 'https://194.182.74.7:3128',
# 'https://212.49.115.67:8080',
# 'https://66.82.123.234:8080',
# 'https://153.149.169.240:3128',
# 'https://96.85.167.3:3128',
# 'https://13.113.23.178:3128',
# 'https://37.122.35.249:8080,'
# 'https://66.82.144.29:8080',
# 'https://45.32.193.119:8118',
# 'https://182.16.248.34:8080',
# 'https://195.190.124.202:8080',
# 'https://81.22.54.60:53281',
# 'https://139.255.57.32:8080',
# 'https://169.239.45.120:53281',
# 'https://51.15.65.152:8080',
# 'https://42.104.84.107:8080',
# 'https://85.187.245.144:53281',
# 'https://154.119.48.155:9999',
# 'https://193.160.224.160:8080',
# 'https://185.111.76.113:53281',
# 'https://185.33.57.31:53281',
# 'https://82.114.65.14:53281',
# 'https://147.75.113.108:8080',
# 'https://74.116.59.8:53281',
# 'https://117.6.161.118:53281',
# 'https://31.25.141.46:53281',
# 'https://116.212.137.235:52335',
# 'https://104.236.48.178:8080',
# 'https://46.216.255.227:8118',
# 'https://187.35.137.97:3128',
# 'https://36.83.79.48:3128',
# 'https://110.77.227.175:62225',
# 'https://192.116.142.153:8080',
# 'https://178.158.204.119:53281',
# 'https://168.205.250.246:53281',
# 'https://131.117.214.38:65103',
#     # ...
# ]

# Enable or disable extensions
# See 'https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See 'https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'wg_test.pipelines.WgTestPipeline': 1,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See 'https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# # The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# # The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

FEED_EXPORT_ENCODING='utf-8'