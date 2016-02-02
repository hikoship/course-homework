from time import clock
from random import uniform
from math import sqrt
from dimension import *
import numpy as np

print '***************************'
print 'Data path:'
print TRAIN_PATH
print TEST_PATH
print '***************************'

# initialization
user_rating = [0 for i in range(USER_NUM)] # average rating of each user (user bias)
user_num = [0 for i in range(USER_NUM)] # number of movies seen by each user
movie_rating = [0 for i in range(MOVIE_NUM)] # average rating of each movie (movie bias)
movie_num = [0 for i in range(MOVIE_NUM)] # number of users that have seen the movie
total_rating = 0 # total rating score of all data
total_num = 0 # total number of clause
p_user = [[uniform(-0.1, 0.1) for i in range(UV_DIMEN)] for j in range(USER_NUM)] # matrix P that M = PQ
q_movie = [[uniform(-0.1, 0.1) for i in range(UV_DIMEN)] for j in range(MOVIE_NUM)] # matrix Q that M = PQ
userIndex = [] # user's ID of each clause
movieIndex = [] # movie's ID of each clause
ratingIndex = [] # rating's ID of each clause

start = clock()

# read data
for line in open(TRAIN_PATH):
    # train dataset file format:
    # USER_ID MOVIE_ID DATE RATING
    info = line.split(',')
    uID = int(info[0]) # user's ID
    mID = int(info[1]) # movie's ID
    rating = int(info[3]) # rating's ID

    userIndex.append(uID)
    movieIndex.append(mID)
    ratingIndex.append(rating)
    
    user_rating[uID] += rating
    user_num[uID] += 1

    movie_rating[mID] += rating
    movie_num[mID] += 1

    total_rating += rating
    total_num += 1

avg_rating = float(total_rating) / total_num  #global average rating
for  i in range(USER_NUM):
    if user_num[i] > 0:
        user_rating[i] = float(user_rating[i]) / user_num[i]
        user_rating[i] -= avg_rating
for i in range(MOVIE_NUM):
    if movie_num[i] > 0:
        movie_rating[i] = float(movie_rating[i]) / movie_num[i]
        movie_rating[i] -= avg_rating


print 'Initialization: ', clock() - start
start = clock()

# iteration

lamda = 0.005
lrate=0.01
min_error = 999999

iterNum = 0
while(True):
    iterNum += 1
    iTime = clock()
    rmse = 0
    print 'iteration: ', iterNum
    for j in range(total_num):
        _u = userIndex[j] # user's ID
        _m = movieIndex[j] # user's ID
        x = [p_user[_u][i] for i in range(UV_DIMEN)] # x = p[_u]
        y = [q_movie[_m][i] for i in range(UV_DIMEN)] # y = q[_m]

        # calculate pq = p[_u].dot(q[_m])
        pq = 0
        for i in range(UV_DIMEN):
            pq += x[i] * y[i]

        error = ratingIndex[j] - pq- user_rating[_u] - movie_rating[_m] - avg_rating
        for i in range(UV_DIMEN):
            p_user[_u][i] += lrate * (error * y[i] - lamda * x[i])
            q_movie[_m][i] += lrate * (error * x[i] - lamda * y[i])
        user_rating[_u] += lrate * (error - lamda * user_rating[_u])
        movie_rating[_m] += lrate * (error - lamda * movie_rating[_m])
        rmse += error * error
        #rmse += error * error + lamda * (user_rating[_u] * user_rating[_u] + movie_rating[_m] * movie_rating[_m] + len_x + len_y)
    rmse /= total_num
    rmse = sqrt(rmse)
    lrate *= 0.95
    print 'rmse = ', rmse
    if abs(min_error - rmse) < TERMINUS:
        break
    if min_error > rmse: min_error = rmse
    print clock() - iTime
        
print 'Iteration: ', clock() - start

# Predict
print 'Predict...'
output = open('predict.txt','w')

for line in open(TEST_PATH):
    info = line.split(',')
    uID = int(info[0])
    mID = int(info[1])
    dID = int(info[2]) / DATE_SPAN

    x = p_user[uID]
    y = q_movie[mID]
    pq = 0
    for i in range(UV_DIMEN):
        pq += x[i] * y[i]
    pred = round(avg_rating + user_rating[uID] + movie_rating[mID] + pq , 1)
    if pred > 5: pred = 5.0
    output.write(str(pred) + '\n')

output.close()
print 'Done.'
