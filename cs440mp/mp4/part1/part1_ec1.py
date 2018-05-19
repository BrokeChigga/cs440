from __future__ import print_function
import numpy as np
import sys
from import_data import import_train_data, import_test_data
from feature_map import feature_map_part1_2

train_raw_digit_dataset = import_train_data("digitdata/trainingimages", "digitdata/traininglabels")
test_raw_digit_dataset = import_test_data("digitdata/testimages", "digitdata/testlabels")

def run_part1_digit_ec1(learning_rate, include_bias, random_init, rand_set, epoch_num, patchdim, overlap):
    print("Importing data...")
    (_, traindata, _, trainlabel) = feature_map_part1_2(train_raw_digit_dataset, {' ': 0, '#': 1, '+': 1}, (28, 28), 10, patchdim, overlap)
    (_, testdata, _, testlabel) = feature_map_part1_2(test_raw_digit_dataset, {' ': 0, '#': 1, '+': 1}, (28, 28), 10, patchdim, overlap)

    # w = np.zeros((10, 28 * 28))
    w = np.random.rand(10, len(traindata[0]))
    bias = np.random.rand(10)

    if (not random_init):
        w = np.zeros((10, len(traindata[0])))
        bias = np.zeros(10)
    if (not include_bias):
        bias = np.zeros(10)
    
    print("Training...")
    trainerr = []
    testerr = []
    for epoch in np.arange(0, epoch_num + 1):
        # Permute the dataset
        p_ind = np.arange(0, len(trainlabel))
        if rand_set:
            p_ind = np.random.permutation(p_ind)
        p_traindata = traindata[p_ind]
        p_trainlabel = trainlabel[p_ind]

        # Epoch test
        preds_test = np.argmax(np.dot(w, testdata.transpose()) + bias.reshape(10, 1), 0)
        preds_train = np.argmax(np.dot(w, traindata.transpose()) + bias.reshape(10, 1), 0)
        trainerr.append(np.sum(preds_train != trainlabel) / (len(trainlabel) * 1.0))
        testerr.append(np.sum(preds_test != testlabel) / (len(testlabel) * 1.0))
        print("Epoch " + str(epoch) + ": " + str(trainerr[epoch] * 100) + "% " + str(testerr[epoch] * 100) + "%", end = '\r')
        sys.stdout.write("\033[K")

        # Train for one epoch
        alpha = learning_rate * 1000.0 / (1000.0 + epoch + 1)
        for (example, label) in zip(p_traindata, p_trainlabel):
            pred = np.argmax(np.dot(w, example) + bias)
            if (pred != label):
                w[label] += alpha * example
                w[pred] -= alpha * example
                if (include_bias):
                    bias[label] += alpha
                    bias[pred] -= alpha
    
    print("Testing")
    preds_test = np.argmax(np.dot(w, testdata.transpose()) + bias.reshape(10, 1), 0)
    print("Accuracy: " + str(np.sum(preds_test == testlabel) / (len(testlabel) * 1.0) * 100) + "%")
    confusion_matrix = np.array([np.array([np.sum(preds_test[testlabel == i] == j) \
                                    for j in np.arange(0, 10)]) \
                                for i in np.arange(0, 10)])
    print('Confusion Matrix:')
    print('\n'.join([''.join(['{:6}'.format(item) for item in row]) for row in confusion_matrix]))

run_part1_digit_ec1(1.0, True, True, True, 200, (2, 4), True)