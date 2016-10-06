lst = [1,2,3]

lst.append(4)

print lst

print ['to','be','or','to','nor','be'].count('to')

a = [1,2,3]
b = [4,5,6]

a.extend(b)

print a

#index methed

kiights = ['We','are','the','knights','who','say','ni']

print kiights.index('who')

#insert list

numbers = [1,2,3,4,5]

numbers.insert(3,'four')

print numbers

numbers.pop()

print numbers

numbers.pop(0)

print numbers

x = ['to','be','or','nor','to','be']

x.remove('be')

print x

x.reverse()

print x

x = [1,5,3,2,6,9,4]

#if  need save the origin list , should do like this y = x[:]
#if do like this  y = x. it dose not effct ,because they point the same place

y = x[:]

y.sort()

print x
print y

#another two parameter key and reserve 









