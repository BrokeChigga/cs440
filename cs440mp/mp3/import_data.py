import numpy as np
import os


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

def extractSingleData(lines, colIndex):
    data = []
    for line in lines:
        data.extend(line[colIndex : colIndex + 10])
    return data


# Return a list of characters without newline for train data in Part2
def import_train_data2(train_data_path):
    file = open(train_data_path)
    lines=file.readlines()

    spaces_counter = 0
    data_counter = 0
    currIndex = 0
    traindata = []

    while(currIndex < 150 and data_counter < 8):
        for line in lines:
            if(line[currIndex].find("%") == -1):
                spaces_counter += 1
            if(spaces_counter > 3):
                data = extractSingleData(lines, currIndex)
                traindata.extend(data)
                spaces_counter = 0
                data_counter += 1
                currIndex += 9
                break
        currIndex += 1
    
    file.close()

    trainlabel = [] 
    labelIndex = 19

    while(labelIndex < 34):
        trainlabel.extend(train_data_path[labelIndex])
        labelIndex += 2

    traindata = np.array(traindata)
    trainlabel = np.array(trainlabel)

    return (traindata, trainlabel)



def get_single_test_data(test_data_path, test_label_path):
    testdata_file = open(test_data_path)
    testdata = np.array(list(testdata_file.read().replace("\n", "")))
    testdata_file.close()
    testlabel_file = open(test_label_path)
    testlabel = np.array(list(testlabel_file.read().replace("\n", "")))
    testlabel_file.close()

    return (testdata, testlabel)


#append data and label into previous list
def insertTestData(path, label_path, data_list, label_list):
    segmented_data = np.array([])
    segmented_label = np.array([])

    for root, dirs, filenames in os.walk(path):
        for f in filenames:
            if(any(i.isdigit() for i in f) == True):
                (data, label) = get_single_test_data(os.path.join(root, f), label_path)
                segmented_data = np.concatenate((segmented_data, data))
                segmented_label = np.concatenate((segmented_label, label))

    retDataList = np.concatenate((data_list, segmented_data))
    retLabelList = np.concatenate((label_list, segmented_label))
    return (retDataList, retLabelList)


# Return a list of characters without newline for test data in Part2
def import_test_data2(test_yes_dir, test_no_dir):
    test_segmented_data = np.array([])
    test_segmented_label = np.array([])

    (test_segmented_data, test_segmented_label) = insertTestData(test_yes_dir, "txt_yesno/yes_test/yes_label.txt", test_segmented_data, test_segmented_label)
    (test_segmented_data, test_segmented_label) = insertTestData(test_no_dir, "txt_yesno/no_test/no_label.txt", test_segmented_data, test_segmented_label)

    return (test_segmented_data, test_segmented_label)


