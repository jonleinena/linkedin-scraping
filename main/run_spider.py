from scrapy.crawler import CrawlerProcess
from linkedin_scraper.linkedin_scraper.spiders.linkedin_spider import LinkedInSpider

process = CrawlerProcess(settings={
    'FEED_FORMAT': 'json',
    'FEED_URI': 'result.json'
})

process.crawl(LinkedInSpider)
process.start()  # the script will block here until the crawling is finished