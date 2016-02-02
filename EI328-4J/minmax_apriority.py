# test: 9150/28636
# train: 27876/59597/23072/2583 - 113128
'''
A:
1
21-24
41-47
61-63
[0, 3721, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 142, 52, 1850, 61, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 556, 87, 262, 260, 684, 119, 4532, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8501, 298, 6751, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

B:
1-9
21-32
41-44
60-68
81-82
[0, 2673, 522, 151, 79, 1437, 225, 265, 630, 770, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1933, 1008, 3756, 1304, 1057, 616, 369, 478, 3585, 209, 207, 1185, 0, 0, 0, 0, 0, 0, 0, 0, 9814, 1634, 435, 185, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9305, 620, 2337, 569, 361, 9480, 1814, 325, 17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 211, 31, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

C:
1-14
21-23
25
30

[0, 987, 1241, 923, 1409, 34, 28, 1985, 6215, 2666, 630, 230, 1249, 6, 2, 0, 0, 0, 0, 0, 0, 708, 1163, 2506, 0, 656, 0, 0, 0, 0, 434, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

D:
1-7
21  

[0, 345, 205, 201, 203, 368, 954, 36, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 271, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
'''

import thread
import time
import Queue
import os
import sys
from liblinearutil import *
#os.system('train heart_scale')

#fn = raw_input('filename')
fn = 'train.txt'

THREAD_NUM_A = 5
THREAD_NUM_B = 11


def svm_read_problem_charLabel(data_file_name):
	"""
	svm_read_problem(data_file_name) -> [y, x]

	Read LIBSVM-format data from data_file_name and return labels y
	and data instances x.
	"""
	prob_y = []
	prob_x = []
	for line in open(data_file_name):
		line = line.split(None, 1)
		# In case an instance with all zero features
		if len(line) == 1: line += ['']
		label, features = line
                if label[0] == 'A': label = 1
                else: label = -1
		xi = {}
		for e in features.split():
			ind, val = e.split(":")
			xi[int(ind)] = float(val)
		prob_y += [float(label)]
		prob_x += [xi]
	return (prob_y, prob_x)

def strToDict(s):
    s.replace(' ', ',')
    return eval('{%s}' % s)

def read_sample_A(index):
    while True:
        label, feature =  qA[index].get().split(None, 1)
        labelA[index] += [1]
        featureA[index] += [eval('{%s}' % feature.replace(' ', ','))  ]      

        countA[index] += 1

def read_sample_B(index):
    while True:
        label, feature =  qB[index].get().split(None, 1)
        labelB[index] += [-1]
        featureB[index] += [eval('{%s}' % feature.replace(' ', ','))]

        countB[index] += 1

def sub_train(thA, thB):
    global task
    label = labelA[thA] + labelB[thB]
    feature = featureA[thA] + featureB[thB]
    prob = problem(label, feature)
    m = train(prob)
    save_model('%s_model_apri_%d_%d/m_%d_%d.model' % (fn, THREAD_NUM_A, THREAD_NUM_B, thA, thB), m)
    mutex.acquire()
    task += 1
    mutex.release()

qA = [Queue.Queue() for n in range(THREAD_NUM_A)] # queue for positive data
qB = [Queue.Queue() for n in range(THREAD_NUM_B)] # queue for negative data

countA = [0 for n in range(THREAD_NUM_A)] # data assigned for each thread
countB = [0 for n in range(THREAD_NUM_B)] # data assigned for each thread

labelA = [[] for n in range(THREAD_NUM_A)] # deposit labels
labelB = [[] for n in range(THREAD_NUM_B)] # deposit labels
featureA = [[] for n in range(THREAD_NUM_A)] # deposit labels
featureB = [[] for n in range(THREAD_NUM_B)] # deposit labels

task = 0


# create threads
for i in range(THREAD_NUM_A):
    thread.start_new_thread(read_sample_A, (i,))

for i in range(THREAD_NUM_B):
    thread.start_new_thread(read_sample_B, (i,))

num_A = 0
num_B = 0
num_C = 0
num_D = 0

start = time.clock()
#for line in open('/Users/gaohongyuan/Documents/4J/train.txt'):

try:
    os.mkdir('%s_model_apri_%d_%d' % (fn, THREAD_NUM_A, THREAD_NUM_B))
except:
    pass

for line in open(fn):
    if line[0] == 'A': 
        num_A += 1
        if int(line[1:3])<=1:
            qA[0].put(line)
        elif int(line[1:3])<=24:
            qA[1].put(line)
        elif int(line[1:3])<=46:
            qA[2].put(line)
        elif int(line[1:3])<=61:
            qA[3].put(line)
        elif int(line[1:3])<=63:
            qA[4].put(line)
    elif line[0] == 'B':
        num_B += 1
        if int(line[1:3])<=9:
            qB[0].put(line)
        elif int(line[1:3])<=27:
            qB[8].put(line)
        elif int(line[1:3])<=32:
            qB[1].put(line)
        elif int(line[1:3])<=44:
            qB[2].put(line)
        elif int(line[1:3])<=63:
            qB[9].put(line)
        elif int(line[1:3])<=68:
            qB[3].put(line)
        elif int(line[1:3])<=82:
            qB[4].put(line)
    elif line[0] == 'C':
        num_C += 1
        if int(line[1:3])<=5:
            qB[10].put(line)
        elif int(line[1:3])<=14:
            qB[5].put(line)
        elif int(line[1:3])<=30:
            qB[6].put(line)
    else:
        num_D += 1
        if int(line[1:3])<=21:
            qB[7].put(line)

        
while True:
    e = True
    for q in qA:
        if not q.empty(): e = False
    for q in qB:
        if not q.empty(): e = False
    if e: break


print time.clock() - start
print countA
print countB
print sum(countA), sum(countB), sum(countA) + sum(countB)
print num_A, num_B, num_C, num_D

# construct problem

mutex = thread.allocate_lock()


for thA in range(THREAD_NUM_A):
    for thB in range(THREAD_NUM_B):
        thread.start_new_thread(sub_train, (thA, thB))

while task < THREAD_NUM_A * THREAD_NUM_B:
    pass

print time.clock() - start

