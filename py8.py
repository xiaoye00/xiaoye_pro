
#string format 

format = "Hello ,%s,%s enough for ya"

values = ('world','Hot')

print format % values

#precision 

format = 'Pi with gree decimals: %.3f'

from math import pi

print format % pi

# format string use tuple only
format = '%d plus %d equals %d' %(1,1,2)

print format

#for string is the max chararicate can be included

format = '%.5s '%'Guido van Rossum'

print format

#the width of the intege , and the precision of the decimal ,if it is not enough to fill whit 0

format = '%010.2f' % pi

print format

#(-) is used to left  align value

format = '%-10.2f' % pi

print format 




