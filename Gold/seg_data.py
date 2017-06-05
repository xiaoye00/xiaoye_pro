#!/usr/bin/env python
#coding:utf8
#############################################################################
##
##  This file is in order to get shanghai huangjin jiaoyisuo data and store it
##
#############################################################################

from web_interface import *
from database_interface import *

class Seg_Interface:

    #initial url to point to SEG official website
    def __init__(self):
        self.url = 'http://www.sge.com.cn/sjzx/mrhqsj'

    def update_data(self,type,table_name):

        #open database
        db = DataBase_Interface('database.sqlite')
        db.connect_db()
        #scan all links
        for i in range(1,19):
            url = 'http://www.sge.com.cn/sjzx/mrhqsj?p=' + str(i)
            web = webInterface(url)
            web.get_context()
            web.context_parser()
            data = web.find_context_inclass('a',['title', 'fs14',  'color333', 'clear'])

            #scan sublinks for detail data
            for rows in data:
                date = rows.find("span",class_='fr').text
                sublink = webInterface('http://www.sge.com.cn' + rows.get('href'))
                sublink.get_context()
                sublink.context_parser()
                silver_data = sublink.find_context_inall('table')
                sub_rows = sublink.find_in_tag('tr',silver_data[0])

                #add silver data to list to ready for storage
                for info in sub_rows:
                    stemp = info.text.split()
                    if stemp[0] == type:
                        stemp.insert(0,date)
                        if len(stemp) != 14:
                            break
                        db.store_data(table_name,stemp)
                        break
        db.commit_db()
        db.close_db()


if __name__ == '__main__':

    seg_data = Seg_Interface()
    #seg_data.update_data('mAu(T+D)','seg_gold')
    seg_data.update_data('Ag(T+D)', 'seg_silver')
    print ('finished')