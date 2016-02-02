from liblinearutil import *

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

preData = 'test.txt'
y, x = svm_read_problem_char(preData)


m = load_model('bigmodel')
a,b,c = predict(y, x, m)

TP = TN = FP = FN = 0
for i in range(len(y)):
    if y[i] > 0 and a[i] > 0: TP += 1
    elif y[i] < 0 and a[i] > 0: FP += 1
    elif y[i] > 0 and a[i] < 0: FN += 1
    elif y[i] < 0 and a[i] < 0: TN += 1


print 'TP: ', TP, 'TN: ' , TN, 'FP: ' , FP, 'FN: ' , FN
