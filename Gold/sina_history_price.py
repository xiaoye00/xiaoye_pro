#!/usr/bin/env python
#coding:utf8
#############################################################################
##
##  for query silver history price
##
#############################################################################

from web_interface import *
from database_interface import *
import datetime
from datetime import timedelta
from web_database import *

class SilverHistoryPrice(WebDataBase):

    #initial url to point to silver history price official website
    def __init__(self):
        WebDataBase.__init__(self, '')
        #self.now_time = datetime.datetime.now().strftime('%Y-%m-%d')
        self.tableName = 'silver_history_price'
        self.now_time = datetime.date.today().strftime('%Y-%m-%d')

        self.start_time = (datetime.date.today() - timedelta(days = 180)).strftime('%Y-%m-%d')



        self.url = 'http://vip.stock.finance.sina.com.cn/q/view/vFutures_History.php?jys=CMX&pz=SI&hy=&breed=SI&type=global&start='+self.start_time+'&end=' +  self.now_time



    def update_data(self):

        #open database
        db = DataBase_Interface('database.sqlite')
        db.connect_db()
        db.set_table(self.tableName)

        web = webInterface(self.url)
        html = web.get_context()
        # s = html.text.encode(html.encoding)
        web.context_parser()
        # , class_ = ['genTbl', 'closedTbl', 'historicalTbl']
        data = web.find_context_inall('table')
        data = data[3].text.split()

        list_len = len(data)

        lastest_date = db.query_data('date', order = 'desc',fetch_no='one')
        self.index = 7
        self.interval = 6
        while( self.index < list_len):
            datelist = data[self.index:self.index+self.interval]
            self.index += self.interval
            if lastest_date != None and lastest_date[0] == datelist[0]:
                break
            db.store_data(datelist)

        db.commit_db()
        db.close_db()

if __name__ == '__main__':

    seg_data = SilverHistoryPrice()
    seg_data.update_data()


    print ('finished')