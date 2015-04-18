# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from store import question
from store import question_profile_db

class QuestionSpiderPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'cnjy':
          question.insert(dict(item))
        elif spider.name == 'question_profile':
          question_profile_db.insert(dict(item))
        return None
