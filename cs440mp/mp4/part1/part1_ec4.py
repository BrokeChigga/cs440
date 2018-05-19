import numpy as np
from sklearn import svm
from import_data import import_train_data, import_test_data
from feature_map import feature_map_part1_1

train_raw_digit_dataset = import_train_data("digitdata/trainingimages", "digitdata/traininglabels")
test_raw_digit_dataset = import_test_data("digitdata/testimages", "digitdata/testlabels")

def run_part1_digit_ec4():
    print("Importing data...")
    (_, traindata, _, trainlabel) = feature_map_part1_1(train_raw_digit_dataset, {' ': 0, '#': 1, '+': 1}, (28, 28), 10)
    (_, testdata, _, testlabel) = feature_map_part1_1(test_raw_digit_dataset, {' ': 0, '#': 1, '+': 1}, (28, 28), 10)
    clf = svm.SVC()

    print("Training...")
    clf.fit(traindata, trainlabel)
    print("Testing")
    preds_test = clf.predict(testdata)

    print("\nAccuracy: " + str(np.sum(preds_test == testlabel) / (len(testlabel) * 1.0) * 100) + "%")
    confusion_matrix = np.array([np.array([np.sum(preds_test[testlabel == i] == j) \
                                    for j in np.arange(0, 10)]) \
                                for i in np.arange(0, 10)])
    print('Confusion Matrix:')
    print('\n'.join([''.join(['{:6}'.format(item) for item in row]) for row in confusion_matrix]))

run_part1_digit_ec4()