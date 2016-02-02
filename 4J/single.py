from liblinearutil import *
from time import clock

trainData = 'heart_scale_multi'

def svm_read_problem_char(data_file_name):
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
                if label[0] == 'A': prob_y += [1]
                else: prob_y += [-1]
		xi = {}
		for e in features.split():
			ind, val = e.split(":")
			xi[int(ind)] = float(val)
		prob_x += [xi]
	return (prob_y, prob_x)
    

start = clock()

y, x = svm_read_problem_char(trainData)

print clock() - start
m = train(y, x)
save_model('heart',m)
print clock() - start



