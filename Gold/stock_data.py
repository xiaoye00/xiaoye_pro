#!/usr/bin/env python
#coding:utf8
#############################################################################
##
##  this file is in order to gather stock data from 163.com
##
#############################################################################


from web_interface import *
from database_interface import *
from web_database import *


class StockData(WebDataBase):

    #initial url to point to silver history price official website
    def __init__(self):
        WebDataBase.__init__(self, '')

        self.url = 'http://quotes.money.163.com/trade/lsjysj_zhishu_000001.html'
        self.tableName = 'stock_data'

    def update_data(self):

        #open database
        db = DataBase_Interface('database.sqlite')
        db.connect_db()
        db.set_table(self.tableName)

        # analyzing the web page
        web = webInterface(self.url)
        html = web.get_context()
        web.context_parser()
        data = web.find_context_inall('table',class_="table_bg001 border_box limit_sale")
        data = data[0].contents


        #getting the newest date from database
        lastest_date = db.query_data('date', order = 'desc',fetch_no='one')

        #setting the first index for data list
        self.index = 3
        self.interval = 1

        #discarding the first three items
        list_len = len(data)#-self.index

        #gather all paga data in this loop
        while( self.index < list_len):
            temp_data_list = data[self.index].contents
            datalist = []
            for temp in temp_data_list:
                datalist.append(temp.text)
            self.index += self.interval
            datalist[0] = datalist[0][:4] + '-'+datalist[0][4:6]+'-'+datalist[0][6:]
            if lastest_date != None and lastest_date[0] == datalist[0]:
                break
            db.store_data(datalist)

        db.commit_db()
        db.close_db()

if __name__ == '__main__':

    seg_data = StockData()
    seg_data.update_data()


    print ('finished')