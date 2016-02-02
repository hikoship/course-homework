import numpy as np
from dimension import *
'''
f = open('train10.txt','w')
i = 0
for line in open('training.txt'):
    if i % 10 == 0:
        f.write(line)
    i += 1

f.close()
'''
'''
i = 0
j = 0
a = {}

f = open('p_user.txt')
f2 = open('p_after.txt', 'w')
while(True):
    line = f.readline()
    line = line.replace('[', '')
    line = line.replace(']', '')
    line = line.split(' ')
    for e in line:
        try:
            e = float(e)
            f2.write(str(e) + '\n')
            j += 1
            print 'j',j
        except:
            pass

    i+=1
    print 'i',i


f.close()
f2.close()

'''
'''
f = open('p_after.txt')
v = []

for i in range(100000):
    for j in range(16):
        e = f.readline()
        v.append(float(e))
        
    print v
    break
    '''

'''
from time import clock
from random import uniform
from math import sqrt

user_rating = [0 for i in range(USER_NUM)]
user_num = [0 for i in range(USER_NUM)]
movie_rating = [0 for i in range(MOVIE_NUM)]
movie_num = [0 for i in range(MOVIE_NUM)]
date_rating = [0 for i in range(DATE_NUM / DATE_SPAN + 1)]
date_num = [0 for i in range(DATE_NUM / DATE_SPAN + 1)]
total_rating = 0
total_num = 0


userIndex = {}
movieIndex = {}
dateIndex = {}
ratingIndex = {}

start = clock()
#uIFile = open('userIndex.txt', 'w')
#mIFile = open('movieIndex.txt', 'w')
#dIFile = open('dateIndex.txt', 'w')
rIFile = open('ratingIndex.txt', 'w')
for line in open('training.txt'):
    info = line.split(',')
#    uIFile.write(str(info[0]) + '\n')
#    mIFile.write(str(info[1]) + '\n')
#    dIFile.write(str(info[2]) + '\n')
    rIFile.write(str(info[3]))

    total_num += 1
print clock() - start
'''
    
r=0
n=0
for line in open('training.txt'):
    n += 1
    r += int(line.split(',')[3])

print float(r)/n

    
