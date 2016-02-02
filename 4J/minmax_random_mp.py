# train: 27876/85252 
# test: 9150/28636
import thread
import time
import Queue
import os
import sys
import multiprocessing
from multiprocessing import Pool, Process
from liblinearutil import *
#os.system('train heart_scale')

THREAD_NUM_A = 5
THREAD_NUM_B = 15


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
        label, feature =  qA.get().split(None, 1)
        labelA[index] += [1]
        featureA[index] += [eval('{%s}' % feature.replace(' ', ','))  ]      

        countA[index] += 1

def read_sample_B(index):
    while True:
        label, feature =  qB.get().split(None, 1)
        labelB[index] += [1]
        featureB[index] += [eval('{%s}' % feature.replace(' ', ','))]

        countB[index] += 1

def sub_train(thA, thB):
    global task
    label = labelA[thA] + labelB[thB]
    feature = featureA[thA] + featureB[thB]
    prob = problem(label, feature)
    m = train(prob)
    save_model('model/m_%d_%d' % (thA, thB), m)
    mutex.acquire()
    task += 1
    mutex.release()

def timecount(start):
    print clock() - start

manager = multiprocessing.Manager()
qA = manager.Queue() # queue for positive data
qB = manager.Queue() # queue for negative data

countA = manager.list([0 for n in range(THREAD_NUM_A)]) # data assigned for each thread
countB = manager.list([0 for n in range(THREAD_NUM_B)]) # data assigned for each thread

labelA = manager.list([[] for n in range(THREAD_NUM_A)]) # deposit labels
labelB = manager.list([[] for n in range(THREAD_NUM_B)]) # deposit labels
featureA = manager.list([[] for n in range(THREAD_NUM_A)] # deposit labels
featureB = manager.list([[] for n in range(THREAD_NUM_B)] # deposit labels

task = 0

dividePool = Pool(processes = THREAD_NUM_A + THREAD_NUM_B)

start = time.clock()

# create threads
for i in range(THREAD_NUM_A):
    dividePool.apply_async(read_sample_A, (i,))
    #thread.start_new_thread(read_sample_A, (i,))

for i in range(THREAD_NUM_B):
    dividePool.apply_async(read_sample_B, (i,))
    #thread.start_new_thread(read_sample_B, (i,))

print 111

num_A = 0
num_B = 0

#for line in open('/Users/gaohongyuan/Documents/4J/train.txt'):
for line in open('train.txt'):
#for line in open('train.txt'):
    if line[0] == 'A': 
        num_A += 1
        qA.put(line)
    else:
        num_B += 1
        qB.put(line)

while not qA.empty() or not qB.empty():
    pass

print 'ok'
dividePool.close()
print 'ok2'

print 'ok3'
print time.clock() - start
print countA
print countB
print sum(countA), sum(countB), sum(countA) + sum(countB)
print num_A, num_B

# construct problem

mutex = thread.allocate_lock()

pool = Pool(processes = THREAD_NUM_A * THREAD_NUM_B)

for thA in range(THREAD_NUM_A):
    for thB in range(THREAD_NUM_B):
        pool.apply_async(sub_train, (thA, thB))
        #p = Process(target = sub_train, args = (thA, thB))
        #p.start()
        #thread.start_new_thread(sub_train, (thA, thB))

pool.close()
pool.join()


print time.clock() - start
