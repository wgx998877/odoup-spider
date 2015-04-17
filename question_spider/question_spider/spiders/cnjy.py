# -*- coding: utf-8 -*-
import scrapy
from question_spider.items import *
import time

class CnjySpider(scrapy.Spider):
  name = "cnjy"
  def __init__(self):
    super(CnjySpider, self).__init__()
    self.allowed_domains = ["tiku.21cnjy.com"]
    self.start_urls = (
      'http://tiku.21cnjy.com/',
    )

  def ExtractTestDiv(self, test_div):
    courses = []
    level = test_div.xpath('h1//text()').extract()[0]
    course_list = test_div.xpath('div[@class="test_container"]/p/a')
    for course in course_list:
      course_name = course.xpath('text()').extract()
      if len(course_name) < 1:
        continue
      url = course.xpath('@href').extract()[0]
      if len(url) < 1:
        continue
      course_tree = CourseTree({
        'name': course_name[0],
        'level': level,
        'url': "http://tiku.21cnjy.com/" + url,
      })
      courses.append(course_tree)
    return courses

  def parse(self, response):
    course_list = response.selector.xpath('//body/div[@class="content"]/div[@id="mainbar"]/div[@class="test"]')
    if len(course_list) < 2:
      return
    junior = self.ExtractTestDiv(course_list[0])
    for course_tree in junior:
      yield scrapy.http.Request(url=course_tree['url'], callback=lambda response, course_tree=course_tree: self.ParseCourseTree(response, course_tree))

    senior = self.ExtractTestDiv(course_list[1])
    for course in senior:
      yield course

  def RecursiveCourseTree(self, tree, tree_dict):
    child_list = tree.xpath('ul/li')
    exam_point = tree.xpath('a/text()').extract()[0]
    url = tree.xpath('a/@href').extract()[0]
    tree_dict['exam_point'] = exam_point
    tree_dict['url'] = "http://tiku.21cnjy.com/" + url
    tree_dict['child_list'] = []
    for child in child_list:
      child_dict = {}
      self.RecursiveCourseTree(child, child_dict)
      tree_dict['child_list'].append(child_dict)
    return tree_dict

  def ParseCourseTree(self, response, course_tree):
    time.sleep(1)
    tree_list = response.selector.xpath('//body/div[@class="content"]/div[@class="shiti_catagory frame"]/ul[@class="treeview"]/li')
    course_list = []
    for tree in tree_list:
      tree_dict = {}
      self.RecursiveCourseTree(tree, tree_dict)
      for key in tree_dict:
        print key, tree_dict[key]
      course_list.append(tree_dict)
      course_tree['course_list'] = course_list
    yield course_tree
