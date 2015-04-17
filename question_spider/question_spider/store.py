#!/usr/bin/env python
# encoding: utf-8

from pymongo import MongoClient

HOST = "127.0.0.1"
PORT = 27017
client = MongoClient(HOST,PORT)
db = client.odoup
question = db.question

def digui(d, tab):
  tab += "--"
  if type(d) == dict:
    for k in d:
      if type(d[k]) != dict and type(d[k]) != list:
        print tab,
        print k,
        print d[k]
      digui(d[k], tab)
  elif type(d) == list:
    for k in d:
      digui(k, tab)
if __name__ == "__main__":
  for i in question.find(level="初中试题", name="数学"):
    digui(i, "")
