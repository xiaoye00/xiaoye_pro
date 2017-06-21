
# !/usr/bin/env python
# coding:utf8

#for analyzing and caculating data and ploting ti


import numpy
from seg_data import *
import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
from pylab import *


from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
from numpy import arange
from etf_data import*
from sina_history_price import *


class AnalysisData:
    """docstring for AnalysisData"""

    def __init__(self):
        print ('initialation')

    def get_data(self, type = 'order',**args):
        if type == 'order':
            self.data = self.obj.get_data(**args)
        else:
            self.data = self.obj.get_datedata(**args)
        return self.data

    def conver_date(self,orignal_date):
        datelist = []
        for date in orignal_date:
            strdate = date[0]
            years = strdate[0:4]
            months = strdate[5:7]
            dates = strdate[8:10]
            datelist.append(datetime.date(int(years), int(months), int(dates)))
        return datelist

    def amplify_data(self, data, argu):
        ret_list = []
        for temp in data:
            ret_list.append(temp * argu)
        return ret_list

    def data_substract(self, data1, data2):
        return list(map(lambda x: x[0] - x[1], zip(data1, data2)))

    def data_add(self, data1, data2):
        return list(map(lambda x: x[0] + x[1], zip(data1, data2)))



class SegGoldDataAnalysis(AnalysisData):
    def __init__(self):
        self.obj =  seg_GoldInterface()
        self.obj.update_data()
        self.datelist = []

    def str2data(self,args):
        temp_list = []
        for data in args:
            temp_list.append( float(data[0].replace(',','')))
        return  temp_list


    def conver_director2data(self):
        dir = self.get_data(name='交收方向', order='asc')
        tempList = []
        for temp in dir:
            tempstr = temp[0][:1]
            if tempstr == '多':
                tempList.append(1)
            else:
                tempList.append(-1)
        return  tempList


    def plot_data(self,date_scope):
        average = self.get_data(name = '加权平均价',order='asc')
        highest_rate = self.get_data(name = '最高价',order='asc')
        lowest_rate = self.get_data(name='最低价', order='asc')
        quantity = self.get_data(name = '成交量',order='asc')
        amplify = self.get_data(name = '涨跌',order='asc')
        amount = self.get_data(name='持仓量', order='asc')
        data_dir = self.conver_director2data()

        date_size  = date_scope+1
        date_range = self.conver_date()
        date_range = date_range[-1:-date_size:-1]
        date_range.reverse()


        average_data = average[-1:-date_size:-1]
        average_data.reverse()
        average_data = self.str2data(average_data)


        highest_rate = highest_rate[-1:-date_size:-1]
        highest_rate.reverse()
        highest_rate = self.str2data(highest_rate)


        lowest_rate = lowest_rate[-1:-date_size:-1]
        lowest_rate.reverse()
        lowest_rate = self.str2data(lowest_rate)


        price_between = self.data_substract(highest_rate,lowest_rate)

        quantity = quantity[-1:-date_size:-1]
        quantity.reverse()
        quantity = self.str2data(quantity)

        amplify = amplify[-1:-date_size:-1]
        amplify.reverse()
        amplify = self.str2data(amplify)

        amount = amount[-1:-date_size:-1]
        amount.reverse()
        amount = self.str2data(amount)
        amount = self.amplify_data(amount,0.001)

        data_dir = data_dir[-1:-date_size:-1]
        data_dir.reverse()


        fig, (ax1,ax2,ax3,ax4,ax5,ax6) = plt.subplots(7,num = 'SegGoldDataAnalysis')
        ax1.plot(date_range, average_data,date_range,highest_rate,date_range,lowest_rate)
        ax1.set_title('Price')



        ax2.plot(date_range,quantity)
        ax2.set_title('Quantity')


        ax3.bar(date_range,amplify)
        ax3.set_title('Amplitude')

        ax4.bar(date_range,price_between)
        ax4.set_title('DataBetween')

        ax5.plot(date_range,amount)
        ax5.set_title('Amount')


        cor = numpy.correlate(amplify, data_dir, "full")
        # cor = numpy.correlate([10,1,1], [1,1,10], "full")
        x = numpy.arange(0, len(cor), 1)

        ax6.plot(x,cor)
        ax6.set_title('corr')
        ax6.grid(True)

        # ax7.bar(date_range,data_dir)
        # ax7.set_title('data_dir')
        # ax7.grid(True)


        fig.autofmt_xdate()
        fig.subplots_adjust(hspace = 0.5)
        fig.show()


class SegSilverDataAnalysis(AnalysisData):
    def __init__(self):
        self.obj = seg_SilverInterface()
        self.datelist = []
        self.obj.update_data()


    def str2data(self, args):
        temp_list = []
        for data in args:
            temp_list.append(float(data[0].replace(',', '')))
        return temp_list


    def conver_director2data(self):
        dir = self.get_data(name='交收方向', order='asc')
        tempList = []
        for temp in dir:
            tempstr = temp[0][:1]
            if tempstr == '多':
                tempList.append(1)
            else:
                tempList.append(-1)
        return tempList

    def plot_data(self,date_scope):

        if isinstance(date_scope,str) == False:

            average = self.get_data(name='加权平均价', order='asc')
            highest_rate = self.get_data(name='最高价', order='asc')
            lowest_rate = self.get_data(name='最低价', order='asc')
            quantity = self.get_data(name='成交量', order='asc')
            amplify = self.get_data(name='涨跌', order='asc')
            amount = self.get_data(name='持仓量', order='asc')
            data_dir = self.conver_director2data()
            orignal_date = self.get_data(name='date', order='asc')

            date_size = date_scope+1
            date_range = self.conver_date(orignal_date)
            date_range = date_range[-1:-date_size:-1]
            date_range.reverse()

            average_data = average[-1:-date_size:-1]
            average_data.reverse()
            average_data = self.str2data(average_data)

            highest_rate = highest_rate[-1:-date_size:-1]
            highest_rate.reverse()
            highest_rate = self.str2data(highest_rate)

            lowest_rate = lowest_rate[-1:-date_size:-1]
            lowest_rate.reverse()
            lowest_rate = self.str2data(lowest_rate)

            price_between = self.data_substract(highest_rate, lowest_rate)

            quantity = quantity[-1:-date_size:-1]
            quantity.reverse()
            quantity = self.str2data(quantity)
            quantity = self.amplify_data(quantity,0.0000001)

            amplify = amplify[-1:-date_size:-1]
            amplify.reverse()
            amplify = self.str2data(amplify)

            amount = amount[-1:-date_size:-1]
            amount.reverse()
            amount = self.str2data(amount)
            amount = self.amplify_data(amount, 0.001)

            data_dir = data_dir[-1:-date_size:-1]
            data_dir.reverse()
        else:
            orignal_date = self.get_data('', name='date', date=date_scope)
            date_range = self.conver_date(orignal_date)
            average_data = self.get_data('', name='加权平均价', date=date_scope)
            average_data = self.str2data(average_data)
            highest_rate = self.get_data('', name='最高价', date=date_scope)
            highest_rate = self.str2data(highest_rate)
            lowest_rate = self.get_data('', name='最低价', date=date_scope)
            lowest_rate = self.str2data(lowest_rate)
            quantity = self.get_data('', name='成交量', date=date_scope)
            quantity = self.str2data(quantity)
            amplify = self.get_data('', name='涨跌', date=date_scope)
            amplify = self.str2data(amplify)
            amount = self.get_data('', name='持仓量', date=date_scope)
            amount = self.str2data(amount)
            price_between = self.data_substract(highest_rate, lowest_rate)





        fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5,num = 'SegSilverDataAnalysis')
        ax1.plot(date_range, average_data)
        ax1.plot(date_range, highest_rate)
        ax1.plot(date_range, lowest_rate)
        ax1.set_title('Rate')

        ax2.plot(date_range, amount)
        ax2.set_title('Inventory Amount')

        ax3.bar(date_range, quantity)
        ax3.set_title('Trading Volume')

        ax4.bar(date_range, amplify)
        ax4.set_title('Rise And Fall Amplitude')

        ax5.bar(date_range, price_between)
        ax5.set_title('Rate Between High And Low')


        # cor = numpy.correlate(average_data, quantity, "full")
        # x = numpy.arange(0, len(cor), 1)

        # ax6.plot(x, cor)
        # ax6.set_title('corr')
        # ax6.grid(True)

        fig.autofmt_xdate()
        fig.subplots_adjust(hspace=0.5)
        fig.show()

class ETF_GoldDataAnalysis(AnalysisData):
    def __init__(self):
        self.obj = ETF_GoldInterface()
        self.obj.update_data()




    def str2data(self, args):
        temp_list = []
        for data in args:
            temp_list.append(float(data[0]))
        return temp_list

    def amplify_data(self, data, argu):
        ret_list = []
        for temp in data:
            ret_list.append(temp * argu)
        return ret_list

    def plot_data(self,date_scope):

        amount = self.get_data(name='净持仓量吨', order='asc')
        amplify = self.get_data(name='增减吨', order='asc')



        date_size = date_scope+1

        date_range = self.conver_date()
        date_range = date_range[-1:-date_size:-1]
        date_range.reverse()

        amount = amount[-1:-date_size:-1]
        amount.reverse()
        amount = self.str2data(amount)

        amplify = amplify[-1:-date_size:-1]
        amplify.reverse()
        amplify = self.str2data(amplify)


        fig, (ax1, ax2) = plt.subplots(2,num = 'ETF_GoldDataAnalysis')
        ax1.plot(date_range, amount)
        ax1.set_title('Amount')

        ax2.bar(date_range, amplify)
        ax2.set_title('Amplify')


        fig.autofmt_xdate()
        fig.subplots_adjust(hspace=0.5)
        fig.show()

class ETF_SilverDataAnalysis(AnalysisData):
    def __init__(self):
        self.obj = ETF_SilverInterface()
        self.obj.update_data()

    def str2data(self, args):
        temp_list = []
        for data in args:
            temp_list.append(float(data[0]))
        return temp_list

    def amplify_data(self, data, argu):
        ret_list = []
        for temp in data:
            ret_list.append(temp * argu)
        return ret_list

    def plot_data(self, date_scope, type = 'order'):

        self.update(date_scope,type)

        fig, (ax1, ax2) = plt.subplots(2,num = 'ETF_SilverDataAnalysis')
        ax1.plot(self.date_range, self.amount)
        ax1.set_title('Amount')

        ax2.bar(self.date_range, self.amplify)
        ax2.set_title('Amplify')

        fig.autofmt_xdate()
        fig.subplots_adjust(hspace=0.5)
        fig.show()

    def update(self,date_scope):

        if isinstance(date_scope,str) == False:

            self.amount = self.get_data(name='净持仓量吨', order='asc')
            self.amplify = self.get_data(name='增减吨', order='asc')
            orignal_date = self.get_data(name='date', order='asc')

            date_size = date_scope + 1
            self.date_range = self.conver_date(orignal_date)
            self.date_range = self.date_range[-1:-date_size:-1]
            self.date_range.reverse()

            self.amount = self.amount[-1:-date_size:-1]
            self.amount.reverse()
            self.amount = self.str2data(self.amount)

            self.amplify = self.amplify[-1:-date_size:-1]
            self.amplify.reverse()
            self.amplify = self.str2data(self.amplify)
        else:
            orignal_date = self.get_data('',name='date', date=date_scope)
            self.amount = self.get_data('',name='净持仓量吨', date=date_scope)
            self.amplify = self.get_data('',name='增减吨', date=date_scope)
            self.amplify = self.str2data(self.amplify)
            self.date_range = self.conver_date(orignal_date)


class CTCF_GoldDataAnalysis(AnalysisData):
    def __init__(self):
        self.obj = CTCF_GoldInterface()
        self.obj.update_data()

    def str2data(self, args):
        temp_list = []
        for data in args:
            temp_list.append(float(data[0]))
        return temp_list

    def amplify_data(self, data, argu):
        ret_list = []
        for temp in data:
            ret_list.append(temp * argu)
        return ret_list

    def plot_data(self, date_scope, show = False):

        self.Duo = self.get_data(name='多头持仓', order='asc')
        self.Kong = self.get_data(name='空头持仓', order='asc')
        self.Duo_Kong = self.get_data(name='多空净持仓', order='asc')
        self.JingKong = self.get_data(name='净空持仓变化', order='asc')

        date_size = date_scope + 1

        self.date_range = self.conver_date()
        self.date_range = self.date_range[-1:-date_size:-1]
        self.date_range.reverse()

        self.Duo = self.Duo[-1:-date_size:-1]
        self.Duo.reverse()
        self.Duo = self.str2data(self.Duo)

        self.Kong = self.Kong[-1:-date_size:-1]
        self.Kong.reverse()
        self.Kong = self.str2data(self.Kong)

        self.Duo_Kong = self.Duo_Kong[-1:-date_size:-1]
        self.Duo_Kong.reverse()
        self.Duo_Kong = self.str2data(self.Duo_Kong)

        self.JingKong = self.JingKong[-1:-date_size:-1]
        self.JingKong.reverse()
        self.JingKong = self.str2data(self.JingKong)

        if show == True:

            fig, (ax1, ax2,ax3,ax4) = plt.subplots(4,num = 'CTCF_GoldDataAnalysis')
            ax1.plot(self.date_range, self.Duo)
            ax1.set_title('Duo')

            ax2.plot(self.date_range, self.Kong)
            ax2.set_title('Kong')

            ax3.plot(self.date_range, self.Duo_Kong)
            ax3.set_title('Duo_Kong')

            ax4.bar(self.date_range, self.JingKong)
            ax4.set_title('JingKong')

            fig.autofmt_xdate()
            fig.subplots_adjust(hspace=0.5)
            fig.show()

class CTCF_SilverDataAnalysis(AnalysisData):
    def __init__(self):
        self.obj = CTCF_SilverInterface()
        self.obj.update_data()

    def str2data(self, args):
        temp_list = []
        for data in args:
            temp_list.append(float(data[0]))
        return temp_list

    def amplify_data(self, data, argu):
        ret_list = []
        for temp in data:
            ret_list.append(temp * argu)
        return ret_list

    def plot_data(self, date_scope, type = 'order'):

        self.update(date_scope,type)

        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4,num = 'CTCF_SilverDataAnalysis')
        ax1.plot(self.date_range, self.Duo)
        ax1.set_title('Duo')

        ax2.plot(self.date_range, self.Kong)
        ax2.set_title('Kong')

        ax3.plot(self.date_range, self.Duo_Kong)
        ax3.set_title('Duo_Kong')

        ax4.bar(self.date_range, self.JingKong)
        ax4.set_title('JingKong')

        fig.autofmt_xdate()
        fig.subplots_adjust(hspace=0.5)
        # fig.suptitle('Errorbar subsampling for better appearance')
        fig.show()

    def update(self,date_scope):

        if isinstance(date_scope, str) == False:

            self.Duo = self.get_data(name='多头持仓', order='asc')
            self.Kong = self.get_data(name='空头持仓', order='asc')
            self.Duo_Kong = self.get_data(name='多空净持仓', order='asc')
            self.JingKong = self.get_data(name='净空持仓变化', order='asc')

            date_size = date_scope + 1

            orignal_date = self.get_data(name='date', order='asc')
            self.date_range = self.conver_date(orignal_date)
            self.date_range = self.date_range[-1:-date_size:-1]
            self.date_range.reverse()

            self.Duo = self.Duo[-1:-date_size:-1]
            self.Duo.reverse()
            self.Duo = self.str2data(self.Duo)

            self.Kong = self.Kong[-1:-date_size:-1]
            self.Kong.reverse()
            self.Kong = self.str2data(self.Kong)

            self.Duo_Kong = self.Duo_Kong[-1:-date_size:-1]
            self.Duo_Kong.reverse()
            self.Duo_Kong = self.str2data(self.Duo_Kong)

            self.JingKong = self.JingKong[-1:-date_size:-1]
            self.JingKong.reverse()
            self.JingKong = self.str2data(self.JingKong)

        else:
            orignal_date = self.get_data('',name='date', date=date_scope)
            self.date_range = self.conver_date(orignal_date)
            self.Duo = self.get_data('',name='多头持仓', date=date_scope)
            self.Kong = self.get_data('',name='空头持仓', date=date_scope)
            self.Duo_Kong = self.get_data('',name='多空净持仓', date=date_scope)
            self.JingKong = self.get_data('',name='净空持仓变化', date=date_scope)

class SilverHistoryRate(AnalysisData):
    def __init__(self):
        self.obj = SilverHistoryPrice()
        self.obj.update_data()


    def str2data(self, args):
        temp_list = []
        for data in args:
            temp_list.append(float(data[0]))
        return temp_list

    def plot_data(self,date_scope):
        self.update(date_scope)

    def update(self,date_scope):

        if isinstance(date_scope, str) == False:
            date_size = date_scope + 1
            orignal_date = self.get_data(name='date', order='asc')
            self.date_range = self.conver_date(orignal_date)
            self.date_range = self.date_range[-1:-date_size:-1]
            self.date_range.reverse()

            self.closing_rate = self.get_data(name='收盘价', order='asc')
            self.closing_rate = self.closing_rate[-1:-date_size:-1]
            self.closing_rate.reverse()
            self.closing_rate = self.str2data(self.closing_rate)

            self.opening_rate = self.get_data(name='开盘价', order='asc')
            self.opening_rate = self.opening_rate[-1:-date_size:-1]
            self.opening_rate.reverse()
            self.opening_rate = self.str2data(self.opening_rate)

            self.high_rate = self.get_data(name='最高价', order='asc')
            self.high_rate = self.high_rate[-1:-date_size:-1]
            self.high_rate.reverse()
            self.high_rate = self.str2data(self.high_rate)

            self.low_rate = self.get_data(name='最低价', order='asc')
            self.low_rate = self.low_rate[-1:-date_size:-1]
            self.low_rate.reverse()
            self.low_rate = self.str2data(self.low_rate)

            self.trading_quantity = self.get_data(name='成交量', order='asc')
            self.trading_quantity = self.trading_quantity[-1:-date_size:-1]
            self.trading_quantity.reverse()
            self.trading_quantity = self.str2data(self.trading_quantity)

        else:
            orignal_date = self.get_data('', name='date', date=date_scope)
            self.date_range = self.conver_date(orignal_date)
            self.closing_rate = self.get_data('', name='收盘价', date=date_scope)
            self.opening_rate = self.get_data('', name='开盘价', date=date_scope)
            self.high_rate = self.get_data('', name='最高价', date=date_scope)
            self.low_rate = self.get_data('', name='最低价', date=date_scope)
            self.trading_quantity = self.get_data('', name='成交量', date=date_scope)
            # "date >= '2017-05-15'"
class SilverAnalysis():
    def __init__(self):
        self.seg = SegSilverDataAnalysis()
        self.etf = ETF_SilverDataAnalysis()
        self.ctcf = CTCF_SilverDataAnalysis()
        self.obj = SilverHistoryRate()
        # self.obj.plot_data(20)


    def plot_data(self):

        #caculate last 30days data
        self.now_time = datetime.date.today().strftime('%Y-%m-%d')
        self.start_time = (datetime.date.today() - timedelta(days = 60)).strftime('%Y-%m-%d')

        #combine parameter
        temp_str = "date >= 'xxxx-xx-xx'"
        date_range = temp_str[0:9] + self.start_time + temp_str[19:len(temp_str)]

        #plot and update parameter
        # self.seg.plot_data(date_range)
        self.seg.plot_data(90)
        self.etf.update(date_range)
        self.ctcf.update(date_range)
        self.obj.update(date_range)

        fig, ax = plt.subplots(6, num='Silver Analysis')
        # draw silver history rate
        # ax[0].plot(self.obj.date_range,self.obj.opening_rate)
        ax[0].plot(self.obj.date_range, self.obj.closing_rate)
        ax[0].plot(self.obj.date_range, self.obj.high_rate,'--')
        ax[0].plot(self.obj.date_range, self.obj.low_rate,'--')
        ax[0].set_title('History Rate')

        #draw ETF history data
        ax[1].bar(self.etf.date_range,self.etf.amplify)
        lineTemp = [0]*len(self.etf.amplify)
        ax[1].plot(self.etf.date_range, lineTemp,'-r')
        ax[1].set_title('ETF Rise And Fall  Amplify')
        ax[2].plot(self.etf.date_range, self.etf.amount)
        ax[2].set_title('ETF Inventory Amount')

        #draw CTCF history data
        ax[3].plot(self.ctcf.date_range,self.ctcf.Duo)
        ax[3].set_title('CTCF Inventory Duo And Kong')
        ax[3].plot(self.ctcf.date_range, self.ctcf.Kong)
        # ax[3].set_title('CTCF Inventory ')
        ax[4].plot(self.ctcf.date_range, self.ctcf.Duo_Kong)
        ax[4].set_title('CTCF Duo_Kong Amplify')
        ax[5].plot(self.ctcf.date_range, self.ctcf.JingKong)
        lineTemp = [0] * len(self.ctcf.JingKong)
        ax[5].plot(self.ctcf.date_range, lineTemp, '-r')
        ax[5].set_title('CTCF JingKong Cariation')




        fig.subplots_adjust(hspace=0.7)


if __name__ == '__main__':

    analysis = SilverAnalysis()
    analysis.plot_data()

    plt.show()