from __future__ import print_function
import numpy as np
import sys
from import_data import import_train_data, import_test_data
from feature_map import feature_map_part1_1
from numpy.linalg import norm
import time

train_raw_digit_dataset = import_train_data("digitdata/trainingimages", "digitdata/traininglabels")
test_raw_digit_dataset = import_test_data("digitdata/testimages", "digitdata/testlabels")

def distance(x1, x2):
    return np.sum(np.power(x1 - x2, 2), 1)

def sin_distance(a, b):
    return np.inner(a, b) / (norm(a) * norm(b))

def manhattan_distance(x,y):
    return sum(abs(a-b) for a,b in zip(x,y))

def run_part1_digit_2(k):
    print("Importing data...")
    (_, traindata, _, trainlabel) = feature_map_part1_1(train_raw_digit_dataset, {' ': 0, '#': 1, '+': 1}, (28, 28), 10)
    (_, testdata, _, testlabel) = feature_map_part1_1(test_raw_digit_dataset, {' ': 0, '#': 1, '+': 1}, (28, 28), 10)

    print("Testing")
    start_time = time.time()
    preds_test = []
    counter = 0
    for (example, data) in zip(testdata, testlabel):
        diffs = distance(example, traindata)
        #diffs = sin_distance(example, traindata)
        #diffs = manhattan_distance(example, traindata)
        idx = np.argsort(diffs)
        neighbor_rank = trainlabel[idx]
        neighbor_rank = neighbor_rank[0:k]
        hist = [np.sum(neighbor_rank[neighbor_rank == i]) for i in np.arange(0, 10)]
        preds_test.append(np.argmax(hist))
        counter += 1
        print(str(counter) + "/" + str(len(testlabel)), end='\r')
        sys.stdout.write("\033[K")
    preds_test = np.array(preds_test)
    print("Accuracy: " + str(np.sum(preds_test == testlabel) / (len(testlabel) * 1.0) * 100) + "%")
    end_time = time.time()
    print('Testing finished in %.3f seconds' % (end_time - start_time))
    confusion_matrix = np.array([np.array([np.sum(preds_test[testlabel == i] == j) \
                                    for j in np.arange(0, 10)]) \
                                for i in np.arange(0, 10)])
    print('Confusion Matrix:')
    print('\n'.join([''.join(['{:6}'.format(item) for item in row]) for row in confusion_matrix]))
run_part1_digit_2(1)

