# train: 27876/85252 
# test: 9150/28636
import thread
import time
import Queue

THREAD_NUM = 20

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

def read_sample(index):
    while True:
        q.get()
        count[index] += 1

q = Queue.Queue() # create a queue for assigning data
count = [0 for n in range(THREAD_NUM)] # data assigned for each thread



# create threads
for i in range(THREAD_NUM):
	thread.start_new_thread(read_sample, (i,))

num_A = 0
num_B = 0
for line in open('/Users/gaohongyuan/Documents/4J/train.txt'):
#for line in open('heart_scale_multi'):
    if line[0] == 'A': num_A += 1
    else: num_B += 1
    q.put(line)

while not q.empty():
    pass

print count
print sum(count)
print num_A, num_B
