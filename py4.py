permissions = 'rw'

ret = 'w' in permissions

print type(ret)


#check user name and PIN code

database = [
    ['albert','1234'],
    ['dilbert','4242'],
    ['smith','7542'],
    ['jons','9843']
]

username = raw_input('User name:')

pin = raw_input('PIN code:')

if [username,pin] in database:
    print 'Access granted'