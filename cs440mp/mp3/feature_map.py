import numpy as np
import itertools

# Mapping from text sequences to integer sequences with 28*28 examples separated
# Ex. ([[" ", "#", "#", "+"], ["#", " ", "+", " "]], [1, 2]) is mapped to
#     ([0, 1, 2], [[0, 1, 1, 2], [1, 0, 2, 0]], [0:9], [1, 2])
def feature_map_part1_1(dataset, dict, dim, max_label):
    (data, label) = dataset
    (dim_h, dim_w) = dim
    data = np.array([dict[w] for w in data]).reshape(int(len(data) / (dim_h * dim_w)), dim_h * dim_w)
    label = np.array([int(i) for i in label])
    var_domain = np.array(list(dict.values()))
    label_domain = np.arange(0, max_label)
    return (var_domain, data, label_domain, label)

def feature_map_part1_2(dataset, dict, dim, max_label, patch_dim, overlap):
    (data, label) = dataset
    (dim_h, dim_w) = dim
    (patch_h, patch_w) = patch_dim
    reshape_data = np.array([dict[w] for w in data]).reshape((int(len(data) / (dim_h * dim_w)), dim_h, dim_w))
    reshape_idx = list(item for item in itertools.product(\
                                    np.arange(0, dim_h - patch_h + 1, 1 if overlap else patch_h), \
                                    np.arange(0, dim_w - patch_w + 1, 1 if overlap else patch_w)))
    
    data = np.array([\
                np.array([int(''.join(map(str, \
                        pixels[row:row+patch_h, col:col+patch_w].flatten()
                    )), base = 2) \
                    for (row, col) in reshape_idx]) \
                for pixels in reshape_data\
            ])
    label = np.array([int(i) for i in label])
    var_domain = np.arange(0, 2 ** (patch_w * patch_h))
    label_domain = np.arange(0, max_label)
    return (var_domain, data, label_domain, label)

def feature_map_part2_2(dataset, dict, dim, max_label):
    (data, label) = dataset
    (dim_h, dim_w) = dim
    data = np.array([dict[w] for w in data]).reshape(int(len(data) / (dim_h * dim_w)), dim_h * dim_w)
    label = np.array([int(i)-1 for i in label])
    var_domain = np.array(list(dict.values()))
    label_domain = np.arange(0, max_label)
    return (var_domain, data, label_domain, label)

def feature_map_part2_extra3(dataset, dict, dim, max_label):
    (data, label) = dataset
    (dim_h, dim_w) = dim
    data = np.array([dict[w] for w in data]).reshape(int(len(data) / (dim_h * dim_w)), dim_h, dim_w)
    temp_list = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            new_row = 1.0*np.sum(data[i][j])/data.shape[2]
            temp_list.append(new_row)
<<<<<<< HEAD
    print("temp_list " + len(temp_list))
    print("dim_h " + dim_h)
    data = np.array(temp_list).reshape(len(temp_list) // dim_h, dim_h)
=======
    data = np.array(temp_list).reshape(int(len(temp_list) / dim_h), dim_h)
>>>>>>> 58d3ef789bca7d86ceec8e72f6932ec9978a7969
    label = np.array([int(i) for i in label])
    var_domain = np.array(list(set(temp_list)))
    label_domain = np.arange(0, max_label)
    return (var_domain, data, label_domain, label)
