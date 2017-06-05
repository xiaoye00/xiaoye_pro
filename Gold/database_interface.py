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

    #connect database
    def connect_db(self):
        self.conn = sqlite3.connect(self.db_name)

    #close database
    def close_db(self):
        self.conn.close()

    #commit database
    def commit_db(self):
        self.conn.commit()

    #store data in multi lines
    def store_data(self,table_name,data_list):

        number_len = ["?"] * len(data_list)

        str = ','.join(number_len)

        table_command = "INSERT INTO " + table_name + " VALUES (" + str +")"

        self.conn.execute(table_command,data_list)



if __name__ == '__main__':

    test_instance = DataBase_Interface('database.sqlite')

    test_instance.connect_db()

    test_instance.store_data('CTCF',['10','2','3','4','5'])

    test_instance.commit_db()

    test_instance.close_db()

    print('finished')