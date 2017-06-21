#!/usr/bin/env python
#coding:utf8
#############################################################################
##
##  This file is in order to operate database storage in SQLite
##
#############################################################################


import sqlite3

class DataBase_Interface:

    def __init__(self,db_name):
        self.db_name = db_name

    def set_table(self,table_name):
        self.table_name = table_name

    #connect database
    def connect_db(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cur = self.conn.cursor()

    #close database
    def close_db(self):
        self.conn.close()

    #commit database
    def commit_db(self):
        self.conn.commit()

    #store data in multi lines
    def store_data(self,data_list):

        number_len = ["?"] * len(data_list)

        str = ','.join(number_len)

        table_command = "INSERT INTO " + self.table_name + " VALUES (" + str +")"

        self.conn.execute(table_command,data_list)

    def query_data(self,name = '*',fetch_no = 'all',order_key = 'date',order=''):
        if order != '':
            query_name = "select " + name + " from " + self.table_name + ' order by '+ order_key +' ' + order  #desc  asc
        else:
            query_name = "select " + name + " from " + self.table_name

        if fetch_no == 'one':
            return  self.conn.execute(query_name).fetchone()
        else:
            return self.conn.execute(query_name).fetchall()

    def query_datedata(self, date,name='*',):
        query_name = "select " + name + " from " + self.table_name + ' where ' + date
        # command = "select * from seg_gold where date >= '2017-06-06'"
        return self.conn.execute(query_name).fetchall()


if __name__ == '__main__':

    test_instance = DataBase_Interface('database.sqlite')

    test_instance.connect_db()

    test_instance.set_table('seg_gold')
    #test_instance.store_data('CTCF',['1','2','3','4','5'])
    data = test_instance.query_datedata("date >= '2017-06-06'")

    # data = test_instance.query_data('date','desc','one')

    # test_instance.commit_db()

    test_instance.close_db()

    print('finished')