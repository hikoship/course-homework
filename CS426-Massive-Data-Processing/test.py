from math import sqrt
import numpy as np

from dimension import *

#user_rating = [0 for i in range(USER_NUM)]
#movie_rating = [0 for i in range(MOVIE_NUM)]

FILENO = raw_input('no.')

user_rating = []
movie_rating = []
date_rating = []
p_user = []
q_movie = []
Npp = []

'''
for line in open('N%s.txt' % FILENO):
    Npp.append(np.array(line.split(' ')))
    pass
    '''


for line in open('user%s.txt' % FILENO):
    user_rating.append(float(line))
    
for line in open('movie%s.txt' % FILENO):
    movie_rating.append(float(line))

#for line in open('date.txt'):
    #date_rating.append(float(line))

for line in open('p_user%s.txt' % FILENO):
    x = []
#    line = line.split('\n')[0]
    info = line.split(' ')
    for i in range(len(info) - 1):
        x.append(float(info[i]))
    p_user.append(np.array(x))

for line in open('q_movie%s.txt' % FILENO):
    x = []
    info = line.split(' ')
    for i in range(len(info) - 1):
        x.append(float(info[i]))
    q_movie.append(np.array(x))

'''
pFile = open('p_after.txt')
for i in range(USER_NUM):
    v = []
    for j in range(16):
        e = pFile.readline()
        v.append(float(e))
    p_user.append(np.array(v))
pFile.close()

qFile = open('q_after.txt')
for i in range(MOVIE_NUM):
    v = []
    for j in range(16):
        e = qFile.readline()
        v.append(float(e))
    q_movie.append(np.array(v))
qFile.close()
'''

avg_rating = 3.60072548945

output = open('5120309623.txt','w')

rmse = 0
num = 0
for line in open('test.txt'):
    info = line.split(',')
    uID = int(info[0])
    mID = int(info[1])
    dID = int(info[2]) / DATE_SPAN
    #pred = round(p_user[uID].dot(q_movie[mID]) , 1)

    pq = 0
    #N_ = 1/sqrt(len(Npp[uID]))
    #pred = round(avg_rating + user_rating[uID] + movie_rating[mID] + pq , 1)
    pred = round(avg_rating + user_rating[uID] + movie_rating[mID] + p_user[uID].dot(q_movie[mID]) , 1)
    #pred = round(avg_rating + user_rating[uID] + movie_rating[mID] + p_user[0][uID] * q_movie[0][mID], 1)
    #pred = round(avg_rating + user_rating[uID] + movie_rating[mID] + p_user[0][uID] * q_movie[0][mID] + p_user[1][uID] * q_movie[1][mID] , 1)
    #pred = round(avg_rating + user_rating[uID] + movie_rating[mID], 1)
    if pred > 5: pred = 5.0
    try:
        score = int(info[3])
    except:
        score = pred
    rmse += (score - pred) * (score - pred)
    output.write(str(pred) + '\n')
    num += 1

rmse = rmse / float(num)
rmse = sqrt(rmse)
print rmse
'''
rmse = 0
num = 0
for line in open('train100.txt'):
    info = line.split(',')
    uID = int(info[0])
    mID = int(info[1])
    dID = int(info[2]) / DATE_SPAN
    pred = round(avg_rating + user_rating[uID] + movie_rating[mID] + date_rating[dID] , 1)
    rmse += (score - pred) * (score - pred)
    output.write(str(pred) + '\n')
rmse = rmse / float(num)
rmse = sqrt(rmse)
print rmse
'''
    
output.close()

print avg_rating
