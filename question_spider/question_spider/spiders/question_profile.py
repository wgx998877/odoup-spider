# -*- coding: utf-8 -*-
import scrapy
import os
from question_spider.items import *
from question_spider.store import *
import time

class QuestionProfileSpider(scrapy.Spider):
  name = "question_profile"
  allowed_domains = ["tiku.21cnjy.com"]
  url_list_file = open("/root/odoup-spider/question_spider/question_spider/spiders/url_list.txt")
  lines = url_list_file.readlines()
  url_list = []
  for line in lines:
    url_list.append(line.strip())
  start_urls = tuple(url_list)

  def parse(self, response):
    questions_list = response.selector.xpath('/html/body/div[@class="content"]/div[@class="shiti_container"]/div[@class="catagory frame shiti_top"]/p')
    if len(questions_list) < 2:
      return
    type_list = questions_list[1].xpath('a')
    if len(type_list) < 2:
      return
    for t in type_list[1:]:
      url = t.xpath('@href').extract()
      if len(url) < 1:
        continue
      type_name = t.xpath('text()').extract()
      if len(type_name) < 1:
        continue
      url = "http://tiku.21cnjy.com/" + url[0]
      type_name = type_name[0]
      yield scrapy.http.Request(url=url, callback=lambda response, question_type=type_name: self.ParseQuestionList(response, question_type))

  # 解析不同的题型的题目列表
  def ParseQuestionList(self, response, question_type):
    questions = response.selector.xpath('/html/body/div[@class="content"]/div[@class="shiti_container"]/div[@class="frame questions"]/div[@class="questions_col"]/ul/li/p[@class="btns"]/a[@class="view_all"]')
    exam_point = response.selector.xpath('/html/body/div[@class="content"]/div[@class="shiti_container"]/div[@class="frame questions"]/h2/b/text()').extract()[0].encode('utf-8')
    exam_point = exam_point.strip().split('：')[1]
    for question in questions:
      url = question.xpath('@href').extract()
      if len(url) < 1:
        continue
      url = "http://tiku.21cnjy.com/" + url[0]
      question_profile = QuestionProfile()
      question_profile['url'] = url
      question_profile['exam_point'] = exam_point
      question_profile['question_type'] = question_type
      yield scrapy.http.Request(url=url, callback=lambda response, question_profile=question_profile: self.ParseQuestionProfile(response, question_profile))

  def ParseQuestionProfile(self, response, question_profile):
    time.sleep(1)
    profile = response.selector.xpath('/html/body/div[@class="content"]/div[@class="shiti_answer"]/div[@class="answer_detail"]')
    if len(profile) < 1:
      self.log("parse question: %s fail!" % resonse.url)
      return
    raw_data = profile[0].extract()
    content = profile.xpath('dl/dt/p//text()').extract()
    des = ""
    for c in content:
      if len(c.strip()) == 0:
        continue
      des += c
    options = profile.xpath('dl/dt/table/tr/td/text()[1]').extract()
    question_profile['option_list'] = []
    for o in options:
      if len(o.strip()) == 0:
        continue
      question_profile['option_list'].append(o)

    answer = profile[0].xpath('dl/dd/p')
    if len(answer) < 2:
      self.log("answer and analysis is not complete: %s" % response.url)
      return
    try:
      question_profile['raw_data'] = raw_data
      question_profile['content'] = des
      question_profile['answer'] = answer[0].xpath('i//text()').extract()[0]
      question_profile['analysis'] = answer[1].xpath('i//text()').extract()[0]
      yield question_profile
    except:
      pass
