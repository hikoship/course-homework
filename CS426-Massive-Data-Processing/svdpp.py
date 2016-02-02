from time import clock
from random import uniform
from math import sqrt
import numpy as np

from dimension import *

FILENO = raw_input('no.')

user_rating = [0 for i in range(USER_NUM)]
user_num = [0 for i in range(USER_NUM)]
movie_rating = [0 for i in range(MOVIE_NUM)]
movie_num = [0 for i in range(MOVIE_NUM)]
date_rating = [0 for i in range(DATE_NUM / DATE_SPAN + 1)]
date_num = [0 for i in range(DATE_NUM / DATE_SPAN + 1)]
total_rating = 0
total_num = 0

# the set of movies seen by a user
Npp = [[] for i in range(USER_NUM)]
# attributes of movies
ypp = [[0 for i in range(UV_DIMEN)] for j in range(MOVIE_NUM)]

#p_user = [[uniform(-0.1, 0.1) for i in range(USER_NUM)] for j in range(UV_DIMEN)]
#q_movie = [[uniform(-0.1, 0.1) for i in range(MOVIE_NUM)] for j in range(UV_DIMEN)]
p_user = [[uniform(-0.1, 0.1) for i in range(UV_DIMEN)] for j in range(USER_NUM)]
q_movie = [[uniform(-0.1, 0.1) for i in range(UV_DIMEN)] for j in range(MOVIE_NUM)]

'''
p_user[0] = [uniform(-0.1, 0.1) for i in range(USER_NUM)]
p_user[1] = [uniform(-0.1, 0.1) for i in range(USER_NUM)]
q_movie[0] = [uniform(-0.1, 0.1) for i in range(MOVIE_NUM)]
q_movie[1] = [uniform(-0.1, 0.1) for i in range(MOVIE_NUM)]
'''

userIndex = []
movieIndex = []
dateIndex = []
ratingIndex = []

start = clock()
for line in open('training.txt'):
    info = line.split(',')
    uID = int(info[0])
    mID = int(info[1])
    dID = int(info[2]) / DATE_SPAN
    rating = int(info[3])

    userIndex.append(uID)
    movieIndex.append(mID)
    dateIndex.append(dID)
    ratingIndex.append(rating)
    
    user_rating[uID] += rating
    user_num[uID] += 1

    movie_rating[mID] += rating
    movie_num[mID] += 1

    #date_rating[dID] += rating
    #date_num[dID] += 1

    total_rating += rating
    total_num += 1

    Npp[uID].append(mID)

avg_rating = 3.6007

userFile = open('user%s.txt' % FILENO,'w')
movieFile = open('movie%s.txt' % FILENO,'w')

for i in range(USER_NUM):
    if user_num[i] == 0:
        user_rating[i] = 0
    else:
        user_rating[i] = float(user_rating[i]) / user_num[i] - avg_rating
    userFile.write(str(user_rating[i])+'\n')

for i in range(MOVIE_NUM):
    if movie_num[i] == 0:
        movie_rating[i] = 0
    else:
        movie_rating[i] = float(movie_rating[i]) / movie_num[i] - avg_rating
    movieFile.write(str(movie_rating[i])+'\n')

print 'Initialization: ', clock() - start
start = clock()

# iteration

lamda = 0.005
gamma=0.01
avg_rating = 3.6007
min_error = 999999

iterNum = 0
#while(True):
for xxx in range(20):
    iterNum += 1
    iTime = clock()
    rmse = 0
    for j in range(total_num):
        _u = userIndex[j]
        _m = movieIndex[j]
#        x = [p_user[_u][i] for i in range(UV_DIMEN)]
#        y = [q_movie[_m][i] for i in range(UV_DIMEN)]
        x = p_user[_u]
        y = q_movie[_m]

        pq = 0
        N_ = 1/sqrt(len(Npp[_u]))
        for i in range(UV_DIMEN):
            #pq += x[i] * (y[i] + N_)
            pq += x[i] * (y[i] + N_ * 0.1)
        error = ratingIndex[j] - pq- user_rating[_u] - movie_rating[_m] - avg_rating
        #error = ratingIndex[j] - user_rating[_u] - movie_rating[_m] - avg_rating
        for i in range(UV_DIMEN):
            p_user[_u][i] += gamma * (error * y[i] - lamda * x[i])
            q_movie[_m][i] += gamma * (error * x[i] - lamda * y[i])

        #avg_rating += gamma * error
        user_rating[_u] += gamma * (error - lamda * user_rating[_u])
        movie_rating[_m] += gamma * (error - lamda * movie_rating[_m])
        rmse += error * error


    rmse /= total_num
    rmse = sqrt(rmse)
    gamma *= 0.95
    print 'rmse = ', rmse
    if abs(min_error - rmse) < 0.0002: break
    '''
    if abs(min_error - rmse) < gamma / 5:
        gamma /= 2
        #lamda /= 2
        pass
        '''
    if min_error > rmse: min_error = rmse
    print clock() - iTime
        
#avgFile = open('avg.txt','w')
#avgFile.write(str(avg_rating))
#avgFile.close()

pFile = open('p_user%s.txt' % FILENO, 'w')
nFile = open('N%s.txt' % FILENO,'w')
#userFile = open('user.txt','w')

for i in range(USER_NUM):
    for j in range (UV_DIMEN):
        pFile.write(str(p_user[i][j]) + ' ')
    pFile.write('\n')

    for j in Npp[i]:
        nFile.write(str(j) + ' ')
    nFile.write('\n')

    #userFile.write(str(user_rating[i])+'\n')
pFile.close()
#userFile.close()

qFile = open('q_movie%s.txt' % FILENO, 'w')
yFile = open('y%s.txt' % FILENO, 'w')
#movieFile = open('movie.txt','w')

for i in range(MOVIE_NUM):
    for j in range (UV_DIMEN):
        qFile.write(str(q_movie[i][j]) + ' ')
        yFile.write(str(ypp[i][j]) + ' ')
    qFile.write('\n')
    yFile.write('\n')

    #movieFile.write(str(movie_rating[i])+'\n')
qFile.close()
#movieFile.close()

print 'Iteration: ', clock() - start
print avg_rating

