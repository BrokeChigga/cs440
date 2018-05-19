import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
from import_data import import_train_data, import_test_data
from import_data import import_train_data2, import_test_data2
from naive_bayes import train, test, evaluation, output_result, run
from feature_map import feature_map_part1_1, feature_map_part1_2
import itertools
import os


#append data and label for train data into previous list
def insertTrainData(path, data_list, label_list):
    segmented_data = np.array([])
    segmented_label = np.array([])

    for root, dirs, filenames in os.walk(path):
        for f in filenames:
            (data, label) = import_train_data2(os.path.join(root, f))
            segmented_data = np.concatenate((segmented_data, data))
            segmented_label = np.concatenate((segmented_label, label))

    retDataList = np.concatenate((data_list, segmented_data))
    retLabelList = np.concatenate((label_list, segmented_label))

    return (retDataList, retLabelList)


#get train dataset
train_segmented_data = np.array([])
train_segmented_label = np.array([])

train_segmented_dataset = insertTrainData('txt_yesno/training', train_segmented_data, train_segmented_label)
test_segmented_dataset = import_test_data2('txt_yesno/yes_test', 'txt_yesno/no_test')

def run_extra_credit_1_audio(k):
    print("================AUDIO - BINARY FEATURE================")
    print("Importing data...")

    train_dataset = feature_map_part1_1(train_segmented_dataset, {' ': 1, '%': 0}, (25, 10), 2)
    test_dataset = feature_map_part1_1(test_segmented_dataset, {' ': 1, '%': 0}, (25, 10), 2)
    
    (model, _, examples, confusion_matrix) = run(k, train_dataset, test_dataset)
    print("=====================================================\n")

run_extra_credit_1_audio(1.0)

