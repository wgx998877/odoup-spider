#!/usr/bin/env python
# encoding: utf-8

from pymongo import MongoClient

HOST = "127.0.0.1"
PORT = 27017
client = MongoClient(HOST,PORT)
db = client.odoup
question = db.question
question_profile_db = db.question_profile
def get_child_list(cl, urllist):
  if cl is None or not isinstance(cl, list):
    return
  for i in cl:
    if 'url' in i and len(i['url'])>0:
      urllist.append(i['url'])
    if 'child_list' in i and len(i['child_list']) > 0:
      get_child_list(i['child_list'], url_list)

if __name__ == "__main__":
  #for i in question.find(level="初中试题", name="数学"):
  #  digui(i, "")
  url_list = []
  for i in question.find():
    if 'course_list' in i:
      for j in i['course_list']:
        get_child_list([j], url_list)

  for url in url_list:
    print url
