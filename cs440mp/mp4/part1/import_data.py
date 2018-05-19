import numpy as np

# Return a list of characters without newline
def import_train_data(train_data_path, train_label_path):
    traindata_file = open(train_data_path)
    traindata = np.array(list(traindata_file.read().replace("\n", "")))
    traindata_file.close()
    trainlabel_file = open(train_label_path)
    trainlabel = np.array(list(trainlabel_file.read().replace("\n", "")))
    trainlabel_file.close()
    return (traindata, trainlabel)

def import_test_data(test_data_path, test_label_path):
    testdata_file = open(test_data_path)
    testdata = np.array(list(testdata_file.read().replace("\n", "")))
    testdata_file.close()
    testlabel_file = open(test_label_path)
    testlabel = np.array(list(testlabel_file.read().replace("\n", "")))
    testlabel_file.close()
    return (testdata, testlabel)