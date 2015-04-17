# -*- coding: utf-8 -*-
import scrapy
from question_spider.items import *
import time

class QuestionProfileSpider(scrapy.Spider):
  name = "question_profile"
  allowed_domains = ["tiku.21cnjy.com"]
  start_urls = (
    'http://tiku.21cnjy.com/tiku.php?mod=quest&channel=2&cid=2&xd=2',
  )

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
      print url + "\t" + type_name
      yield scrapy.http.Request(url=url, callback=lambda response: self.ParseQuestionList(response))
      break

  def ParseQuestionList(self, response):
    questions = response.selector.xpath('/html/body/div[@class="content"]/div[@class="shiti_container"]/div[@class="frame questions"]/div[@class="questions_col"]/ul/li/p[@class="btns"]/a[@class="view_all"]')
    for question in questions:
      url = question.xpath('@href').extract()
      if len(url) < 1:
        continue
      url = "http://tiku.21cnjy.com/" + url[0]
      print url
      yield scrapy.http.Request(url=url, callback=lambda response: self.ParseQuestionProfile(response))

  def ParseQuestionProfile(self, response):
    profile = response.selector.xpath('/html/body/div[@class="content"]/div[@class="shiti_answer"]/div[@class="answer_detail"]/dl')
    content = profile.xpath('dt//*[(td|tr)]//text()').extract()
    for c in content:
      print c
