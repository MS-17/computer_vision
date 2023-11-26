import matplotlib.pyplot as plt
import numpy as np


# check if a point is not 0
def check(B, y, x):
    if not 0 <= x < B.shape[0]:
        return False
    if not 0 <= y < B.shape[1]:
        return False
    if B[y, x] != 0:
        return True
    return False


# get neighbours for the current point
def neighbors2(B, y, x):
    left = y, x-1
    top = y - 1, x
    if not check(B, *left):
        left = None
    if not check(B, *top):
        top = None
    return left, top


# False if there's no left and top neighbour 
def exists(neighbors):
    return not all([n is None for n in neighbors])


# let's say linked is the following array: 
# labels: 0 1 2 3 4
# linked: 0 2 4 0 3
# find(2, linked) returns 3 (j = 2 => linked[2] = 4 => j = 4 => linked[4] = 3 =>
# j = 3 => linked[j] = 0 => stop => return 3)
# this function finds the connected to the label point via some middle point
def find(label, linked):
    j = label
    while linked[j] != 0:
        j = linked[j]
    return j


# if label1 is not connected to label2 connect them
def union(label1, label2, linked):
    j = find(label1, linked)
    k = find(label2, linked)
    if j != k:
        linked[k] = j


def two_pass_labeling(B):
    # assign to all non-zero pixels the value = -1
    B = (B.copy() * - 1).astype("int")
    # print(B)
    # print(B.shape)

    # linked components (we'll need it for the second iteration of the algorithm)
    linked = np.zeros(len(B), dtype="uint")
    
    # a result of the function
    labels = np.zeros_like(B)

    # the first label
    label = 1

    # iterate over all rows and cols and if a pixel is not 0 get its neighbours
    # then if there's no left and top neighbour assign a new label to 'm' and increment the total 
    # number of labels, otherwise iterate over the neighbours and get the minimum label of the neighbour and assign it to 'm'
    # finally assign label ('m') to the current position
    # Then iterate over neighbours and if a neighbour exists get its label, check if it's equal to the 
    # label of the current point and if not, call union() 
    for row in range(B.shape[0]):
        for col in range(B.shape[1]):
            if B[row, col] != 0:
                n = neighbors2(B, row, col)
                if not exists(n):
                    m = label
                    label += 1
                else:
                    lbs = [labels[i] for i in n if i is not None]
                    # print(n, lbs)
                    m = min(lbs)
                labels[row, col] = m
                for i in n:
                    if i is not None:
                        lb = labels[i]
                        if lb != m:
                            union(m, lb, linked)

    # print(labels)
    # print(linked)
    # plt.imshow(labels)
    # plt.show()

    # iterate one more time to finally connect everything
    for row in range(B.shape[0]):
        for col in range(B.shape[1]):
            if B[row, col] != 0:
                new_label = find(labels[row, col], linked)
                if new_label != labels[row, col]:
                    labels[row, col] = new_label


    # todo organize labels correctly

    return labels


if __name__ == "__main__":
    image = np.zeros((20, 20), dtype='int32')
    
    image[1:-1, -2] = 1
    
    image[1, 1:5] = 1
    image[1, 7:12] = 1
    image[2, 1:3] = 1
    image[2, 6:8] = 1
    image[3:4, 1:7] = 1
    
    image[7:11, 11] = 1
    image[7:11, 14] = 1
    image[10:15, 10:15] = 1
    
    image[5:10, 5] = 1
    image[5:10, 6] = 1

    labeled_image = two_pass_labeling(image)
    
    plt.figure(figsize=(12, 5))
    plt.subplot(121)
    plt.imshow(image)
    plt.subplot(122)
    plt.imshow(labeled_image.astype("uint8"))
    plt.show()