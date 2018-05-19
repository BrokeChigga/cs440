from __future__ import print_function
import numpy as np
import sys
import matplotlib.pyplot as plt
from matplotlib import ticker
from import_data import import_train_data, import_test_data
from feature_map import feature_map_part1_1

train_raw_digit_dataset = import_train_data("digitdata/trainingimages", "digitdata/traininglabels")
test_raw_digit_dataset = import_test_data("digitdata/testimages", "digitdata/testlabels")

def run_part1_digit_1(learning_rate, include_bias, random_init, rand_set, epoch_num):
    print("Importing data...")
    (_, traindata, _, trainlabel) = feature_map_part1_1(train_raw_digit_dataset, {' ': 0, '#': 1, '+': 1}, (28, 28), 10)
    (_, testdata, _, testlabel) = feature_map_part1_1(test_raw_digit_dataset, {' ': 0, '#': 1, '+': 1}, (28, 28), 10)

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
        # print(traindata.shape)
        # print(p_traindata.shape)
        # print(trainlabel.shape)
        # print(p_trainlabel.shape)
        # print(p_ind.shape)
        # break

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

    # Plot learning curve
    fig1 = plt.figure(figsize=(10,6))
    plt.plot(np.arange(0, epoch_num + 1), trainerr, label = 'Training Error')
    plt.plot(np.arange(0, epoch_num + 1), testerr, label = 'Testing Error')
    plt.xlabel('Epoch', fontsize = 14)
    plt.ylabel('Error rate', fontsize = 14)
    plt.xlim(xmin = 0, xmax = epoch_num)
    plt.ylim(ymin = 0, ymax = 1)
    plt.legend()
    plt.grid(True)
    plt.title('Learning Curves', fontsize = 16)

    # EC 2
    fig2, axes1 = plt.subplots(nrows=2, ncols=5, figsize=(10,6))
    fig2.subplots_adjust(left=0.03, right=0.95, top=0.93, bottom=0.05, wspace=0.30, hspace=0.05)
    for i in np.arange(0, 5):
        axstop = axes1[0][i]
        axsbot = axes1[1][i]
        imtop = axstop.imshow(np.reshape(w[i], (28, 28)), interpolation = 'nearest', cmap="jet")
        imbot = axsbot.imshow(np.reshape(w[i + 5], (28, 28)), interpolation = 'nearest', cmap="jet")
        axstop.set_title(str(i))
        axsbot.set_title(str(i + 5))
        axstop.set_axis_off()
        axsbot.set_axis_off()
        cbartop = plt.colorbar(imtop, ax=axstop, fraction=0.046, pad=0.04)
        cbartop.locator = ticker.MaxNLocator(nbins=5)
        cbartop.update_ticks()
        cbarbot = plt.colorbar(imbot, ax=axsbot, fraction=0.046, pad=0.04)
        cbarbot.locator = ticker.MaxNLocator(nbins=5)
        cbarbot.update_ticks()
    plt.suptitle('Weight Vectors Visualization', fontsize=16)

    plt.show()

run_part1_digit_1(10.0, True, False, True, 100)




