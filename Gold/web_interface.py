#!/usr/bin/env python
#coding:utf8
#############################################################################
##
##  This file is in order to get real time data from web page
##
#############################################################################

from bs4 import BeautifulSoup
import requests , re
import sqlite3

class webInterface:
    """docstring for Web Interface"""
    def __init__(self,url):
        self.url = url

    #get web page context
    def get_context(self):
        self.html = requests.get(self.url)
        self.html = self.html.text.encode(self.html.encoding)
        return self.html

    #do web context parse
    def context_parser(self):
        self.sp = BeautifulSoup(self.html,'html.parser')
        return self.sp

    #look for the context in all
    def find_context_inall(self,context,**args):
        return self.sp.find_all(context, **args)

    #look for context
    def find_context(self,context,sp):
        return sp.find_all(context)

    #look for a string in all
    def regex_query(self,context):
        return re.findall(context,self.html)

    def find_in_tag(self,context,tag):
        return tag.find_all(context)




if __name__ == '__main__':
    test_instance = webInterface('http://www.sge.com.cn/sjzx/mrhqsj')

    context = test_instance.get_context()

    sp = test_instance.context_parser()

    testdata = test_instance.find_context_inclass_too('a',class_=['title', 'fs14',  'color333', 'clear'])

    print ('finished')

