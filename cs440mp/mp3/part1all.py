import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
from import_data import import_train_data, import_test_data
from naive_bayes import train, test, evaluation, output_result, run
from feature_map import feature_map_part1_1, feature_map_part1_2

train_raw_digit_dataset = import_train_data("digitdata/trainingimages", "digitdata/traininglabels")
test_raw_digit_dataset = import_test_data("digitdata/testimages", "digitdata/testlabels")
train_raw_face_dataset = import_train_data("facedata/facedatatrain", "facedata/facedatatrainlabels")
test_raw_face_dataset = import_test_data("facedata/facedatatest", "facedata/facedatatestlabels")

# Returns the n largest indices from a numpy array
def largest_indices(ary, n):
    flat = ary.flatten()
    indices = np.argpartition(flat, -n)[-n:]
    indices = indices[np.argsort(-flat[indices])]
    return np.unravel_index(indices, ary.shape)

def run_part1_digit_1(k):
    print("================DIGIT - BINARY FEATURE================")
    print("Importing data...")
    train_dataset = feature_map_part1_1(train_raw_digit_dataset, {' ': 0, '#': 1, '+': 1}, (28, 28), 10)
    test_dataset = feature_map_part1_1(test_raw_digit_dataset, {' ': 0, '#': 1, '+': 1}, (28, 28), 10)

    (model, _, examples, confusion_matrix) = run(0.1, train_dataset, test_dataset)

    confusion_matrix_ndig = np.array(confusion_matrix)
    np.fill_diagonal(confusion_matrix_ndig, 0)
    confusion_pairs = largest_indices(confusion_matrix_ndig, 4)
    confusion_pairs = list(zip(confusion_pairs[0], confusion_pairs[1]))

    (priors, distributions) = model

    fig1, axes1 = plt.subplots(nrows=5, ncols=4, figsize=(6,7.5))
    fig1.subplots_adjust(left=0.07, right=0.92, top=0.93, bottom=0.05, wspace=0.05, hspace=0.05)
    for i in np.arange(0, 5):
        axs = axes1[i]
        ims = [axs[0].imshow(np.reshape(1-examples[2*i][0], (28, 28)), interpolation = 'nearest', cmap="Greys"), \
                axs[1].imshow(np.reshape(1-examples[2*i][1], (28, 28)), interpolation = 'nearest', cmap="Greys"), \
                axs[2].imshow(np.reshape(1-examples[2*i+1][0], (28, 28)), interpolation = 'nearest', cmap="Greys"), \
                axs[3].imshow(np.reshape(1-examples[2*i+1][1], (28, 28)), interpolation = 'nearest', cmap="Greys")]
        for j in np.arange(0, 4):
            axs[j].set_axis_off()
    plt.suptitle('Example Pairs with Lowest(left) and Highest(right) posterior probability', fontsize=12)

    fig2, axes2 = plt.subplots(nrows=4, ncols=3, figsize=(6,8))
    fig2.subplots_adjust(left=0.05, right=0.92, top=0.95, bottom=0.05, wspace=0.35, hspace=0.01)
    for pairi in np.arange(0, 4):
        axs = axes2[pairi]
        logp1 = np.log(np.array([ d[1] for d in distributions[confusion_pairs[pairi][0]] ]))
        logp2 = np.log(np.array([ d[1] for d in distributions[confusion_pairs[pairi][1]] ]))
        ims = [axs[0].imshow(np.reshape(logp1, (28, 28)), interpolation = 'nearest', cmap='jet'), \
                axs[1].imshow(np.reshape(logp2, (28, 28)), interpolation = 'nearest', cmap='jet'), \
                axs[2].imshow(np.reshape(logp1 - logp2, (28, 28)), interpolation = 'nearest', cmap='jet')]
        for j in np.arange(0, 3):
            axs[j].set_axis_off()
            cbar = plt.colorbar(ims[j], ax=axs[j], fraction=0.046, pad=0.04)
            cbar.locator = ticker.MaxNLocator(nbins=5)
            cbar.update_ticks()
    plt.suptitle('Odds ratios', fontsize=16)
    plt.show()

    print("=====================================================\n")

def run_part1_digit_2(k, h, w, overlap):
    if (overlap):
        print("===========DIGIT - PIXEL GROUP (%d * %d) OVERLAP==========" % (h, w))
    else:
        print("===============DIGIT - PIXEL GROUP (%d * %d) =============" % (h, w))
    print("Importing data...")

    train_dataset = feature_map_part1_2(train_raw_digit_dataset, {' ': 0, '#': 1, '+': 1}, (28, 28), 10, (h, w), overlap)
    test_dataset = feature_map_part1_2(test_raw_digit_dataset, {' ': 0, '#': 1, '+': 1}, (28, 28), 10, (h, w), overlap)

    run(0.1, train_dataset, test_dataset)

    print("=====================================================\n")


def run_part1_digit_extra_1(k):
    print("================DIGIT - TERNARY FEATURE================")
    print("Importing data...")

    train_dataset = feature_map_part1_1(train_raw_digit_dataset, {' ': 0, '#': 1, '+': 2}, (28, 28), 10)
    test_dataset = feature_map_part1_1(test_raw_digit_dataset, {' ': 0, '#': 1, '+': 2}, (28, 28), 10)

    run(0.1, train_dataset, test_dataset)

    print("=====================================================\n")

def run_part1_face_1(k):
    print("================FACE - BINARY FEATURE================")
    print("Importing data...")

    train_dataset = feature_map_part1_1(train_raw_face_dataset, {' ': 0, '#': 1}, (70, 60), 2)
    test_dataset = feature_map_part1_1(test_raw_face_dataset, {' ': 0, '#': 1}, (70, 60), 2)

    run(0.1, train_dataset, test_dataset)

    print("=====================================================\n")

def run_part1_face_2(k, h, w, overlap):
    if (overlap):
        print("===========FACE - PIXEL GROUP (%d * %d) OVERLAP==========" % (h, w))
    else:
        print("===============FACE - PIXEL GROUP (%d * %d) =============" % (h, w))
    print("Importing data...")

    train_dataset = feature_map_part1_2(train_raw_face_dataset, {' ': 0, '#': 1}, (70, 60), 2, (h, w), overlap)
    test_dataset = feature_map_part1_2(test_raw_face_dataset, {' ': 0, '#': 1}, (70, 60), 2, (h, w), overlap)

    run(0.1, train_dataset, test_dataset)
    print("=====================================================\n")



run_part1_digit_1(0.1)

run_part1_digit_2(0.1, 2, 2, False)
run_part1_digit_2(0.1, 2, 4, False)
run_part1_digit_2(0.1, 4, 2, False)
run_part1_digit_2(0.1, 4, 4, False)

run_part1_digit_2(0.1, 2, 2, True)
run_part1_digit_2(0.1, 2, 4, True)
run_part1_digit_2(0.1, 4, 2, True)
run_part1_digit_2(0.1, 4, 4, True)
run_part1_digit_2(0.1, 2, 3, True)
run_part1_digit_2(0.1, 3, 2, True)
run_part1_digit_2(0.1, 3, 3, True)

run_part1_digit_extra_1(0.1)

run_part1_face_1(0.1)

run_part1_face_2(0.1, 2, 2, False)
run_part1_face_2(0.1, 2, 4, False)
run_part1_face_2(0.1, 4, 2, False)
run_part1_face_2(0.1, 4, 4, False)

run_part1_face_2(0.1, 2, 2, True)
run_part1_face_2(0.1, 2, 4, True)
run_part1_face_2(0.1, 4, 2, True)
run_part1_face_2(0.1, 4, 4, True)
run_part1_face_2(0.1, 2, 3, True)
run_part1_face_2(0.1, 3, 2, True)
run_part1_face_2(0.1, 3, 3, True)
