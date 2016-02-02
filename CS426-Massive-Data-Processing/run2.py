from time import clock
from random import uniform
from math import sqrt

from dimension import *

FILENO = raw_input('no.')

# initialization
user_rating = [0 for i in range(USER_NUM)] # average rating of each user
user_num = [0 for i in range(USER_NUM)] # number of movies seen by each user
movie_rating = [0 for i in range(MOVIE_NUM)] # average rating of each movie
movie_num = [0 for i in range(MOVIE_NUM)] # number of users that have seen the movie
date_rating = [0 for i in range(DATE_NUM / DATE_SPAN + 1)] 
date_num = [0 for i in range(DATE_NUM / DATE_SPAN + 1)]
total_rating = 0 # total rating score of all data
total_num = 0 # total number of clause
p_user = [[uniform(-0.1, 0.1) for i in range(UV_DIMEN)] for j in range(USER_NUM)] # matrix P that M = PQ
q_movie = [[uniform(-0.1, 0.1) for i in range(UV_DIMEN)] for j in range(MOVIE_NUM)] # matrix Q that M = PQ
userIndex = [] # user's ID of each clause
movieIndex = [] # movie's ID of each clause
dateIndex = [] # date's ID of each clause
ratingIndex = [] # rating's ID of each clause

start = clock()

# read data
for line in open('training1000.txt'):
    # train dataset file format:
    # USER_ID MOVIE_ID DATE RATING
    info = line.split(',')
    uID = int(info[0]) # user's ID
    mID = int(info[1]) # movie's ID
    dID = int(info[2]) / DATE_SPAN #date's ID
    rating = int(info[3]) # rating's ID

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

avg_rating = float(total_rating) / total_num  #global average rating

userFile = open('user%s.txt' % FILENO,'w')
movieFile = open('movie%s.txt' % FILENO,'w')

print 'Initialization: ', clock() - start
start = clock()

# iteration

lamda = 0.005
gamma=0.01
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

        pq = 0
        '''
        len_x = 0
        len_y = 0
        '''

        # calculate pq = p[_u].dot(q[_m])
        for i in range(UV_DIMEN):
            pq += x[i] * y[i]
            '''
            len_x += x[i] * x[i]
            len_y += y[i] * y[i]
            '''

        error = ratingIndex[j] - pq- user_rating[_u] - movie_rating[_m] - avg_rating
        for i in range(UV_DIMEN):
            p_user[_u][i] += gamma * (error * y[i] - lamda * x[i])
            q_movie[_m][i] += gamma * (error * x[i] - lamda * y[i])
        user_rating[_u] += gamma * (error - lamda * user_rating[_u]) * 2
        movie_rating[_m] += gamma * (error - lamda * movie_rating[_m]) * 2
        rmse += error * error
        #rmse += error * error + lamda * (user_rating[_u] * user_rating[_u] + movie_rating[_m] * movie_rating[_m] + len_x + len_y)
    rmse /= total_num
    rmse = sqrt(rmse)
    print 'rmse = ', rmse
    if abs(min_error - rmse) < 0.0001:
        break
    '''
    if abs(min_error - rmse) < gamma / 5:
        gamma /= 2
        #lamda /= 2
        pass
        '''
    if min_error > rmse: min_error = rmse
    print clock() - iTime
        
pFile = open('p_user%s.txt' % FILENO, 'w')
userFile = open('user%s.txt' % FILENO, 'w')
for i in range(USER_NUM):
    for j in range (UV_DIMEN):
        pFile.write(str(p_user[i][j]) + ' ')
    pFile.write('\n')
    userFile.write(str(user_rating[i])+'\n')
pFile.close()
userFile.close()

qFile = open('q_movie%s.txt' % FILENO, 'w')
movieFile = open('movie%s.txt' % FILENO, 'w')
for i in range(MOVIE_NUM):
    for j in range (UV_DIMEN):
        qFile.write(str(q_movie[i][j]) + ' ')
    qFile.write('\n')
    movieFile.write(str(movie_rating[i])+'\n')
qFile.close()
movieFile.close()

print 'Iteration: ', clock() - start
print avg_rating

