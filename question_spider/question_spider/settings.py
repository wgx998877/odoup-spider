# -*- coding: utf-8 -*-

# Scrapy settings for question_spider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'odoup_question'

SPIDER_MODULES = ['question_spider.spiders']
NEWSPIDER_MODULE = 'question_spider.spiders'
ITEM_PIPELINES = {
  'question_spider.pipelines.QuestionSpiderPipeline': 100,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'question_spider (+http://www.yourdomain.com)'
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36'
