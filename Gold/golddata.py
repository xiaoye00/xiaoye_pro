#!/usr/bin/env python
#coding:utf8
from bs4 import BeautifulSoup
import requests , re
import sqlite3

class GoldInfo:
    """docstring for Hotel"""
    def __init__(self):
        url = 'http://www.sge.com.cn/sjzx/mrhqsj/5141674?top=789398439266459648'
        html = requests.get(url).text
        sp = BeautifulSoup(html,'html.parser')
        data = sp.find_all('table')
        rows = data[0].find_all('tr')
        self.dataList = []
        for info in rows:
            stemp = info.text.split()
            self.dataList.append(stemp)
        self.silver_list = []
    def get_data(self):
        return self.dataList

    def store_data_once(self,date,data):
        self.conn = sqlite3.connect('golddata.sqlite')
        data.insert(0,date)
        self.conn.execute("insert into database values (?, ?,?, ?,?, ?,?, ?,?, ?,?, ?,?)", data)
        self.conn.commit()
        self.conn.close()

    def store_data_manytimes(self,data):
        self.conn = sqlite3.connect('golddata.sqlite')
        self.conn.executemany("insert into database values (?, ?,?, ?,?, ?,?, ?,?, ?,?, ?,?,?)", data)
        self.conn.commit()
        self.conn.close()

    def regex_query(self):
        url = 'http://www.sge.com.cn/sjzx/mrhqsj'
        html = requests.get(url).text
        regex = r'([2][0]\w\w-\w\w-\w\w)'
        date = re.findall(regex,html)
        print (date)

    def update_data(self):
        #scan all links
        for i in range(1,19):
            #url = 'http://www.sge.com.cn/sjzx/mrhqsj?p =' + str(i)
            url = 'http://www.sge.com.cn/sjzx/mrhqsj?p='+ str(i)
            html = requests.get(url).text
            sp = BeautifulSoup(html,'html.parser')
            class_list = ['title', 'fs14',  'color333', 'clear']
            data = sp.find_all('a',class_=class_list)
            print(str(i))
            #scan sublinks for detail data
            for rows in data:
                date = rows.find("span",class_='fr')
                date = date.text
                link = 'http://www.sge.com.cn' + rows.get('href')
                subHtml = requests.get(link).text
                subSp = BeautifulSoup(subHtml, 'html.parser')
                silver_data = subSp.find_all('table')
                sub_rows = silver_data[0].find_all('tr')

                #add silver data to list to ready for storage
                for info in sub_rows:
                    stemp = info.text.split()
                    if stemp[0] == 'Ag(T+D)':
                        stemp.insert(0,date)
                        if len(stemp) != 14:
                            break
                        stuple = tuple(stemp)
                        self.silver_list.append(stuple)
                        break
            self.store_data_manytimes(self.silver_list)
            self.silver_list.clear()

    def query_database(self,name):
        self.conn = sqlite3.connect('golddata.sqlite')
        query_name = "select " + name + " from database"
        return self.conn.execute(query_name)
    
if __name__ == '__main__':
    stdroom = GoldInfo()
    big_room = GoldInfo()
    print (stdroom.get_data())
    #stdroom.store_data()
    #stdroom.update_data()
    stdroom.query_database("Quantity")
    # print (stdroom.cacl_all())
    # print (big_room.cacl_all())
    # print (big_room.cacl_all())
