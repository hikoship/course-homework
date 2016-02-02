from time import clock
from random import uniform
from math import sqrt
import numpy as np

from dimension import *

user_rating = [0 for i in range(USER_NUM)]
user_num = [0 for i in range(USER_NUM)]
movie_rating = [0 for i in range(MOVIE_NUM)]
movie_num = [0 for i in range(MOVIE_NUM)]
date_rating = [0 for i in range(DATE_NUM / DATE_SPAN + 1)]
date_num = [0 for i in range(DATE_NUM / DATE_SPAN + 1)]
total_rating = 0
total_num = 0

p_user = [uniform(-0.1, 0.1) for i in range(USER_NUM)]
q_movie = [uniform(-0.1, 0.1) for i in range(MOVIE_NUM)]

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

    total_num += 1




print 'Initialization: ', clock() - start
start = clock()

# iteration

lamda = 0.1
gamma=0.02
avg_rating = 3.6
min_error = 999999
#for i in range(10): # iterate 10 times
while(True):
    rmse = 0
    print 'iteration: ', i + 1
    for j in range(total_num):
        _u = userIndex[j]
        _m = movieIndex[j]
        x = p_user[_u]
        y = q_movie[_m]
        error = ratingIndex[j] - x * y - user_rating[_u] - movie_rating[_m] - avg_rating
        p_user[_u] += gamma * (error * y - lamda * x)
        q_movie[_m] += gamma * (error * x - lamda * y)
        avg_rating += gamma * error
        user_rating[_u] += gamma * (error - lamda * user_rating[_u]) * 2
        movie_rating[_m] += gamma * (error - lamda * movie_rating[_m]) * 2
        rmse += error * error
    rmse /= total_num
    rmse = sqrt(rmse)
    print 'rmse = ', rmse
    if abs(min_error - rmse) < 0.0001: break
    if abs(min_error - rmse) < gamma / 2:
        gamma /= 2
        #lamda /= 2
    if min_error > rmse: min_error = rmse
        
avgFile = open('avg.txt','w')
avgFile.write(str(avg_rating))
avgFile.close()

pFile = open('p_user.txt', 'w')
userFile = open('user.txt','w')

for i in range(USER_NUM):
    pFile.write(str(p_user[i]) + '\n')
    userFile.write(str(user_rating[i])+'\n')
pFile.close()
userFile.close()

qFile = open('q_movie.txt', 'w')
movieFile = open('movie.txt','w')

for i in range(MOVIE_NUM):
    qFile.write(str(q_movie[i]) + '\n')
    movieFile.write(str(movie_rating[i])+'\n')
qFile.close()
movieFile.close()

print 'Iteration: ', clock() - start
print avg_rating

