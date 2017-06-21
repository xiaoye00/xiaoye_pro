#!/usr/bin/env python
#coding:utf8
#############################################################################
##
##  This file is in order to get shanghai huangjin jiaoyisuo data and store it
##
#############################################################################

from web_interface import *
from database_interface import *
from web_database import *

class Seg_Interface(WebDataBase):

    #initial url to point to SEG official website
    def __init__(self,datatype):

        WebDataBase.__init__(self,datatype)

        self.url = 'http://www.sge.com.cn/sjzx/mrhqsj'

        if self.dataType == 'mAu(T+D)':
            self.tableName = 'seg_gold'
        else:
            self.tableName = 'seg_silver'


    def update_data(self):

        #open database
        db = DataBase_Interface('database.sqlite')
        db.connect_db()
        db.set_table(self.tableName)

        #scan all links
        findOutFlag = 0
        for i in range(1,19):

            if findOutFlag == 1:
                break

            url = 'http://www.sge.com.cn/sjzx/mrhqsj?p=' + str(i)
            web = webInterface(url)
            web.get_context()
            web.context_parser()
            data = web.find_context_inall('a',class_=['title', 'fs14',  'color333', 'clear'])

            #findOutFlag

            #query lastest date
            lastest_date = db.query_data('date', order = 'desc',fetch_no='one')
            #scan sublinks for detail data
            for rows in data:

                #if reach the latest date , quit store data
                if findOutFlag == 1:
                    break
                #begin update data
                date = rows.find("span",class_='fr').text
                sublink = webInterface('http://www.sge.com.cn' + rows.get('href'))
                sublink.get_context()
                sublink.context_parser()
                silver_data = sublink.find_context_inall('table')
                sub_rows = sublink.find_in_tag('tr',silver_data[0])

                #add silver data to list to ready for storage
                for info in sub_rows:
                    stemp = info.text.split()
                    if stemp[0] == self.dataType:
                        stemp.insert(0,date)
                        if len(stemp) != 14:
                            break
                       #compare the latest data
                        if len(lastest_date) != 0 and lastest_date[0] == date:
                            findOutFlag = 1
                            break
                        db.store_data(stemp)
                        break
        db.commit_db()
        db.close_db()


class seg_GoldInterface(Seg_Interface):
    def __init__(self):
        Seg_Interface.__init__(self,'mAu(T+D)')

class seg_SilverInterface(Seg_Interface):
    def __init__(self):
        Seg_Interface.__init__(self,'Ag(T+D)')


if __name__ == '__main__':

    seg_data = seg_SilverInterface()
    seg_data.update_data()
    seg_data = seg_GoldInterface()
    seg_data.update_data()



    print ('finished')