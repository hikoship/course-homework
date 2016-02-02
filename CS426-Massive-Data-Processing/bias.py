from time import clock
from random import uniform

from dimension import *

user_rating = [0 for i in range(USER_NUM)]
user_num = [0 for i in range(USER_NUM)]
movie_rating = [0 for i in range(MOVIE_NUM)]
movie_num = [0 for i in range(MOVIE_NUM)]
date_rating = [0 for i in range(DATE_NUM / DATE_SPAN + 1)]
date_num = [0 for i in range(DATE_NUM / DATE_SPAN + 1)]
total_rating = 0
total_num = 0

p_user = [uniform(-1, 1) for i in range(USER_NUM)]
q_movie = [uniform(-1, 1) for i in range(MOVIE_NUM)]

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

    date_rating[dID] += rating
    date_num[dID] += 1

    total_rating += rating
    total_num += 1

print clock() - start
start = clock()

#get average
avg_rating = float(total_rating) / total_num

avgFile = open('avg.txt','w')
avgFile.write(str(avg_rating))
avgFile.close()

userFile = open('user.txt','w')
movieFile = open('movie.txt','w')
dateFile = open('date.txt','w')

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

for i in range(DATE_NUM / DATE_SPAN + 1):
    if date_num[i] == 0:
        date_rating[i] = 0
    else:
        date_rating[i] = float(date_rating[i]) / date_num[i] - avg_rating
    dateFile.write(str(date_rating[i])+'\n')

userFile.close()
movieFile.close()
dateFile.close()

print 'Initialization: ', clock() - start
start = clock()

# iteration

lamda = 0.05
gamma=0.01
for i in range(10): # iterate 10 times
    print 'iteration: ', i + 1
    for j in range(total_num):
        _u = userIndex[j]
        _m = movieIndex[j]
        x = p_user[_u]
        y = q_movie[_m]
        error = ratingIndex[j] - x * y - user_rating[_u] - movie_rating[_m] - avg_rating
        p_user[_u] += gamma * (error * y - lamda * x)
        q_movie[_m] += gamma * (error * x - lamda * y)

pFile = open('p_user.txt', 'w')
for i in range(USER_NUM):
    pFile.write(str(p_user[i]) + '\n')
pFile.close()

qFile = open('q_movie.txt', 'w')
for i in range(MOVIE_NUM):
    qFile.write(str(q_movie[i]) + '\n')
qFile.close()

print avg_rating
print 'Iteration: ', clock() - start


