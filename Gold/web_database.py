#!/usr/bin/env python
#coding:utf8
#############################################################################
##
##  This file is as a basic class for web data
##
#############################################################################

from web_interface import *
from database_interface import *


class WebDataBase:
    def __init__(self,datatype):
        self.dataType = datatype

    def update_data(self):
        return 1

    # name = '*',fetch_no = 'all',order_key = 'date',order=''
    def get_data(self,**argus):
        #open database
        db = DataBase_Interface('database.sqlite')
        db.connect_db()
        db.set_table(self.tableName)
        data = db.query_data(**argus)
        db.close_db()
        return data

    def get_datedata(self,date,name = '*'):
        db = DataBase_Interface('database.sqlite')
        db.connect_db()
        db.set_table(self.tableName)
        data = db.query_datedata(date,name)
        db.close_db()
        return data
