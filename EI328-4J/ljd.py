import os
import multiprocessing
import time

def train(train_name, model_name, test_name, output_name):
    a = './train '+train_name
    b = './predict '+test_name+' '+model_name+' '+output_name
    p1 = os.popen(a,'r')
    p2 = os.popen(b,'r')

if __name__ == "__main__":
    time_start = time.time()
    p1 = multiprocessing.Process(target=train, args=('train.txt','train.txt.model','test.txt','output.txt'))
    p2 = multiprocessing.Process(target=train, args=('train.txt','train.txt.model','test.txt','output.txt'))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    time_end = time.time()
    print time_end-time_start
