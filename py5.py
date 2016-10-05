#exchange the value in list

x = [1,1,1]

x[1] = 2

print x


#delete elemate of list

names = ['Alice','Beth','Celil','Dee-Dee','Earl']

del names[2]

print names 

#assign value by pieaces

name = list('Perl')

name[2:] = list('ar')

print name

numbers = [1,5]

numbers[1:1] = [2,3,4]

print numbers

numbers[1:4] = []

print numbers