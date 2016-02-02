from time import clock

USER_NUM = 100000
MOVIE_NUM = 17770
DATE_NUM = 5115
DATE_SPAN = 30

user_rating = [0 for i in range(USER_NUM)]
user_num = [0 for i in range(USER_NUM)]
movie_rating = [0 for i in range(MOVIE_NUM)]
movie_num = [0 for i in range(MOVIE_NUM)]
date_rating = [0 for i in range(DATE_NUM / DATE_SPAN + 1)]
date_num = [0 for i in range(DATE_NUM / DATE_SPAN + 1)]
total_rating = 0
total_num = 0

start = clock()
for line in open('training.txt'):
    info = line.split(',')
    uID = int(info[0])
    mID = int(info[1])
    dID = int(info[2]) / DATE_SPAN
    rating = int(info[3])

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

print avg_rating
print clock() - start


