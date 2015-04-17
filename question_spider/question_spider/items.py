# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CourseNode(scrapy.Item):
  # 考点
  exam_point = scrapy.Field()
  # url
  url = scrapy.Field()

class CourseTree(scrapy.Item):
  # 课程名字，例如语文、数学
  name = scrapy.Field()
  # 级别，例如初中、高中
  level = scrapy.Field()
  # 对应的题库url
  url = scrapy.Field()
  course_list = scrapy.Field()

class QuestionProfile(scrapy.Item):
  # 题目内容
  content = scrapy.Field()
  # 答案
  answer = scrapy.Field()
  # 题目对应的url
  url = scrapy.Field()
  # 题型
  question_type = scrapy.Field()

class Questions(scrapy.Item):
  # 题目列表，用每道题的url存
  questions = scrapy.Field()
  # 题型
  question_type = scrapy.Field()
  # url
  url = scrapy.Field()

class ExamPoint(scrapy.Item):
  exam_point = scrapy.Field()
  url = scrapy.Field()
  questions_list = scrapy.Field()
