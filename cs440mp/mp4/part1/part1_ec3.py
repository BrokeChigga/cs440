from __future__ import print_function
import numpy as np
import sys
from import_data import import_train_data, import_test_data
from feature_map import feature_map_part1_1

train_raw_digit_dataset = import_train_data("digitdata/trainingimages", "digitdata/traininglabels")
test_raw_digit_dataset = import_test_data("digitdata/testimages", "digitdata/testlabels")

def softmax(ylin):
    exp = np.exp(ylin - np.max(ylin, 0))
    norms = np.sum(exp, axis=0).reshape((-1, 1))
    return (exp.T / norms).T

def cross_entropy(yhat, y):
    return -np.sum(y * np.log(yhat), axis=0)

def net(X, W):
    y_linear = np.dot(W, X)
    yhat = softmax(y_linear)
    return yhat

def run_part1_digit_ec3(learning_rate, include_bias, random_init, rand_set, epoch_num):
    print("Importing data...")
    (_, traindata, _, trainlabel) = feature_map_part1_1(train_raw_digit_dataset, {' ': 0, '#': 1, '+': 1}, (28, 28), 10)
    (_, testdata, _, testlabel) = feature_map_part1_1(test_raw_digit_dataset, {' ': 0, '#': 1, '+': 1}, (28, 28), 10)

    if include_bias:
        traindata = np.hstack((traindata, np.ones((len(traindata), 1))))
        testdata = np.hstack((testdata, np.ones((len(testdata), 1))))

    # w = np.zeros((10, 28 * 28))
    w = np.random.rand(10, len(traindata[0]))

    traindata = (traindata - np.reshape(np.mean(traindata, 1), (len(traindata), 1))) / np.reshape(np.max(traindata, 1) - np.min(traindata, 1), (len(traindata), 1))
    testdata = (testdata - np.reshape(np.mean(testdata, 1), (len(testdata), 1))) / np.reshape(np.max(testdata, 1) - np.min(testdata, 1), (len(testdata), 1))

    if (not random_init):
        w = np.zeros((10, len(traindata[0])))
    
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
        preds_test = np.argmax(net(testdata.transpose(), w), 0)
        preds_train = np.argmax(net(traindata.transpose(), w), 0)
        trainerr.append(np.sum(preds_train != trainlabel) / (len(trainlabel) * 1.0))
        testerr.append(np.sum(preds_test != testlabel) / (len(testlabel) * 1.0))
        print("Epoch " + str(epoch) + ": " + str(trainerr[epoch] * 100) + "% " + str(testerr[epoch] * 100) + "%", end = '\r')
        sys.stdout.write("\033[K")

        # Train for one epoch
        alpha = learning_rate * 1000.0 / (1000.0 + epoch + 1)

        grad_t = np.zeros(w.shape)
        bias_t = np.zeros(10)
        for (example, label) in zip(p_traindata, p_trainlabel):
            ylinear = np.dot(w, example)
            exp_vals = np.exp(ylinear - np.max(ylinear))
            lik = exp_vals[label] / np.sum(exp_vals)
            grad_t[label, :] += example * (1 - lik)
        w = w + alpha * grad_t
    
    print("Testing")
    preds_test = np.argmax(net(testdata.transpose(), w), 0)
    print("Accuracy: " + str(np.sum(preds_test == testlabel) / (len(testlabel) * 1.0) * 100) + "%")
    confusion_matrix = np.array([np.array([np.sum(preds_test[testlabel == i] == j) \
                                    for j in np.arange(0, 10)]) \
                                for i in np.arange(0, 10)])
    print('Confusion Matrix:')
    print('\n'.join([''.join(['{:6}'.format(item) for item in row]) for row in confusion_matrix]))

run_part1_digit_ec3(10.0, True, True, True, 100)

