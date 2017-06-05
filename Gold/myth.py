
# !/usr/bin/env python
# coding:utf8



import matplotlib.pyplot as pt
from webdata import *
import numpy

class AnalysisData:
    """docstring for AnalysisData"""

    def __init__(self):
        print ('initialation')

    def get_data(self,name):
       gold_info = GoldInfo()
       silverData = gold_info.query_database(name)
       silverData = self.string_to_float(silverData)
       return silverData
       # lenght = len(silverData)
       # silverDate = numpy.arange(0,lenght,1)
       # pt.plot(silverDate,silverData)
       # pt.show()
    def string_to_float(self,data):
        dataList = []
        for temp in data:
            dataList.append(float(temp[0].replace(',','')))
        return dataList

    def plot_data(self,y,title='',max_line = 1,index = 1,color_= '',line_style='line'):
        ax = pt.subplot(max_line, 1, index)
        x = len(y)
        x = numpy.arange(0,x,1)
        y.reverse()
        if color_ != '':
            if line_style == 'line':
                pt.plot(x, y,color = color_)
            else:
                pt.bar(x, y, color=color_)
        else:
            if line_style == 'line':
                pt.plot(x, y)
            else:
                pt.bar(x, y)
        pt.title(title)



if __name__ == '__main__':
    analysis = AnalysisData()

    max_line = 10
    i = 1
    # analysis.plot_data(analysis.get_data('Quantity'),'Quantity',max_line,i)
    # i += 1
    analysis.plot_data(analysis.get_data('Volume'),'Volume',max_line,i)
    # i += 1
    # analysis.plot_data(analysis.get_data('closingPrice'), 'closingPrice',max_line, i)
    # i += 1
    # analysis.plot_data(analysis.get_data('openingRate'), 'openingRate', max_line, i)
    i += 1
    analysis.plot_data(analysis.get_data('Average'), 'Average', max_line, i)
    i += 1
    analysis.plot_data(analysis.get_data('H_L'), 'H_L', max_line, i,'red','bar')
    i += 1
    analysis.plot_data(analysis.get_data('Inventory'), 'Inventory', max_line, i,'green')

    pt.show()