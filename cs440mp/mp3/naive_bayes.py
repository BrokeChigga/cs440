import time
import numpy as np

# Train the model, return value consists of priors and distributions
# Each distribution is a list of dictionary
# Ex. ([prior1, prior2, ...], 
#       [
#           [{feat1: prob, feat2: prob, ...}, {feat1: prob, feat2: prob, ...}, ...
#       ], 
#       [
#           [{feat1: prob, feat2: prob, ...}, {feat1: prob, feat2: prob, ...}, ...
#       ],
#       ...
#     ])
def train(dataset, k):
    (domain, traindata, label_domain, trainlabel) = dataset
    model = (\
                np.array([(len(trainlabel[trainlabel == i]) / (len(trainlabel) + 1.0)) \
                    for i in np.arange(0, len(label_domain))]), \
                np.array([\
                    [ dict(zip(domain, p_feat)) for p_feat in np.transpose(np.array([\
                        np.array((np.sum(traindata[trainlabel == i, :] == ran_val, 0) + k) / \
                                        (len(trainlabel[trainlabel == i]) + k * len(domain))) \
                        for ran_val in domain ]\
                    ))] \
                    for i in np.arange(0, len(label_domain))\
                ])\
            )
    return model

# log(prior | class) + sum[log(P(feature=val|class))] for all class and find the max index
def test(model, dataset):
    (_, testdata, label_domain, testlabel) = dataset
    (priors, distributions) = model
    posteriors = np.array([\
                np.array([\
                    np.sum(np.log(np.array([d[pval] for (pval, d) in zip(inputpixel, ppixeldicts)]))) \
                        for (pclass, ppixeldicts) in zip(priors, distributions)\
                ]) for inputpixel in testdata\
            ])
    probs = posteriors + np.log(priors)
    preds = np.argmax(probs, 1)

    examples = np.array([\
                (testdata[testlabel == i][np.argmin(posteriors[testlabel == i, i])], \
                testdata[testlabel == i][np.argmax(posteriors[testlabel == i, i])])
                for i in np.arange(0, len(label_domain))\
            ])\

    return (preds, examples)


# Return the confusion matrix
def evaluation(predictions, dataset):
    (_, _, label_domain, testlabel) = dataset
    confusion_matrix = np.array([np.array([np.sum(predictions[testlabel == i] == j) \
                                    for j in np.arange(0, len(label_domain))]) \
                                for i in np.arange(0, len(label_domain))])
    
    return confusion_matrix

# Output accuracy and confusion matrix
def output_result(model, confusion_matrix):
    print(('Overall accuracy: %.3f' % (np.trace(confusion_matrix) * 1.0 / np.sum(np.sum(confusion_matrix)) * 100)) + "%")
    print([('%.3f' % (percent * 100)) + "%" for percent in (np.diagonal(confusion_matrix) / (1.0 * np.sum(confusion_matrix, 1)))])
    print('\nConfusion Matrix:')
    print('\n'.join([''.join(['{:6}'.format(item) for item in row]) for row in confusion_matrix]))

def run(k, train_dataset, test_dataset):
    print("Training...")
    start_time = time.time()
    model = train(train_dataset, k)
    end_time = time.time()
    print('Training finished in %.3f seconds' % (end_time - start_time))

    print("Testing...")
    start_time = time.time()
    (preds, examples) = test(model, test_dataset)
    end_time = time.time()
    print('Testing finished in %.3f seconds' % (end_time - start_time))

    confusion_matrix = evaluation(preds, test_dataset)
    output_result(model, confusion_matrix)
    return (model, preds, examples, confusion_matrix)
