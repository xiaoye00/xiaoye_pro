#!/usr/bin/env python
#coding:utf8
#############################################################################
##
##  This file is in order to get ETF data and store it
##
#############################################################################

from web_interface import *
from database_interface import *
from web_database import *
class ETF_Interface(WebDataBase):

    #initial url to point to SEG official website
    def __init__(self,datatype):
        WebDataBase.__init__(self,datatype)

        if self.dataType == 'etf_gold':
            self.url = 'http://www.dyhjw.com/dyhjw/etf.html'
            self.index = 6
            self.interval = 6
            self.tableName = 'ETF_Gold'
        elif self.dataType == 'etf_silver':
            self.url = 'http://www.dyhjw.com/html/hangqing/etf/slv_etf.php'
            self.index = 6
            self.interval = 6
            self.tableName = 'ETF_Silver'
        elif self.dataType == 'ctcf_gold':
            self.url = 'http://www.dyhjw.com/dyhjw/cftc.html'
            self.index = 5
            self.interval = 5
            self.tableName = 'CTCF_Gold'
        else:
            self.url = 'http://www.dyhjw.com/dyhjw/cftc_silver.html'
            self.index = 5
            self.interval = 5
            self.tableName = 'CTCF_Silver'

    def update_data(self):

        #open database
        db = DataBase_Interface('database.sqlite')
        db.connect_db()
        db.set_table(self.tableName)


        web = webInterface(self.url)
        web.get_context()
        web.context_parser()
        data = web.find_context_inall('table',class_='sx_table')
        data = data[0].text.split('\n')

        while(True):
            if '' in data:
                data.remove('')
            elif ' ' in data:
                data.remove(' ')
            else:
                break

        list_len = len(data)

        lastest_date = db.query_data('date', order = 'desc',fetch_no='one')

        while( self.index < list_len):
            datelist = data[self.index:self.index+self.interval]
            self.index += self.interval
            datelist[0] = datelist[0].replace('年','-')
            datelist[0] = datelist[0].replace('月', '-')
            datelist[0] = datelist[0].replace('日', '')
            if lastest_date != None and lastest_date[0] == datelist[0]:
                break
            db.store_data(datelist)

        db.commit_db()
        db.close_db()

class ETF_GoldInterface(ETF_Interface):
    def __init__(self):
        ETF_Interface.__init__(self,'etf_gold')

class ETF_SilverInterface(ETF_Interface):
    def __init__(self):
        ETF_Interface.__init__(self,'etf_silver')

class CTCF_GoldInterface(ETF_Interface):
    def __init__(self):
        ETF_Interface.__init__(self,'ctcf_gold')

class CTCF_SilverInterface(ETF_Interface):
    def __init__(self):
        ETF_Interface.__init__(self,'ctcf_silver')

if __name__ == '__main__':

    seg_data = CTCF_SilverInterface()
    seg_data.update_data()
    data = seg_data.get_data()

    print ('finished')