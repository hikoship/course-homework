from liblinearutil import *
from ctypes import c_double

trainData = 'train.txt'
preData = 'test.txt'
sPOS_NUM = raw_input('a')
sNEG_NUM = raw_input('b')
POS_NUM = int(sPOS_NUM)
NEG_NUM = int(sNEG_NUM)
print 'ok'

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
    
def predict_iter(y, x, m, posNum, negNum):
	def info(s):
		print(s)

	solver_type = m[0][0].param.solver_type
	nr_class = m[0][0].get_nr_class()
	nr_feature = m[0][0].get_nr_feature()
	is_prob_model = m[0][0].is_probability_model()
	bias = m[0][0].bias
	if bias >= 0:
		biasterm = feature_node(nr_feature+1, bias)
	else:
		biasterm = feature_node(-1, bias)

        #gaohongyuan
        if nr_class <= 2:
                nr_classifier = 1
        else:
                nr_classifier = nr_class
        dec_values = (c_double * nr_classifier)()

        max_labels = []

        min_labels = []

        # max
        for pos in range(posNum):
            # min
            min_labels = []
            for neg in range(negNum):
	        pred_labels = []
                for xi in x:
                        xi, idx = gen_feature_nodearray(xi, feature_max=nr_feature)
                        xi[-2] = biasterm
                        label = liblinear.predict_values(m[pos][neg], xi, dec_values)
                        pred_labels += [label]
                # merge pred_labels
                if neg == 0:
                    min_labels = pred_labels
                else:
                    for i in range(len(min_labels)):
                        if min_labels[i] > pred_labels[i]:
                            min_labels[i] = pred_labels[i]
            if pos == 0:
                max_labels = min_labels
            else:
                for i in range(len(max_labels)):
                    if max_labels[i] < min_labels[i]:
                        max_labels[i] = 1.0

	if len(y) == 0:
		y = [0] * len(x)
	ACC, MSE, SCC = evaluations(y, max_labels)
	l = len(y)
	if m[0][0].is_regression_model():
		info("Mean squared error = %g (regression)" % MSE)
		info("Squared correlation coefficient = %g (regression)" % SCC)
	else:
		info("Accuracy = %g%% (%d/%d) (classification)" % (ACC, int(l*ACC/100), l))

	return max_labels

y, x = svm_read_problem_char(preData)

m = []


for pos in range(POS_NUM):
    m.append([])
    for neg in range(NEG_NUM):
        m[pos] += [load_model('%s_model_apri_%d_%d/m_%d_%d.model' % (trainData, POS_NUM, NEG_NUM, pos, neg))]

print 'load finish'
a = predict_iter(y,x,m,POS_NUM,NEG_NUM)



TP = TN = FP = FN = 0
for i in range(len(y)):
    if y[i] > 0 and a[i] > 0: TP += 1
    elif y[i] < 0 and a[i] > 0: FP += 1
    elif y[i] > 0 and a[i] < 0: FN += 1
    elif y[i] < 0 and a[i] < 0: TN += 1


print 'TP: ', TP, 'TN: ' , TN, 'FP: ' , FP, 'FN: ' , FN
