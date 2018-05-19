import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
from import_data import import_train_data, import_test_data
from naive_bayes import train, test, evaluation, output_result, run

from feature_map import feature_map_part2_2


train_audio_dataset = import_train_data("mfccdata/training_data.txt", "mfccdata/training_labels.txt")
test_audio_dataset = import_test_data("mfccdata/testing_data.txt", "mfccdata/testing_labels.txt")

def run_part22_audio(k):
	print("================MFC - BINARY FEATURE================")
	print("Importing data...")

	train_dataset = feature_map_part2_2(train_audio_dataset, {' ': 1, '%': 0}, (30, 13), 5)
	test_dataset = feature_map_part2_2(test_audio_dataset, {' ': 1, '%': 0}, (30, 13), 5)

	run(k, train_dataset, test_dataset)    
	print("===================================================\n")

run_part22_audio(0.1)
run_part22_audio(0.5)
run_part22_audio(1.0)
run_part22_audio(5.0)
run_part22_audio(10.0)
run_part22_audio(20.0)