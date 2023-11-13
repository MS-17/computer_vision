import numpy as np
import matplotlib.pyplot as plt

def check(B, y, x): #is valid point
    return y >= 0 and x >= 0 and B[y, x]

def neighbours2(B, y, x):
    left = y, x-1
    top = y-1, x
    if not check(B, *left):
        left = None
    if not check(B, *top):
        top = None
    return left, top

def find(label, linked): #найти минимальный несвязанный label
    j = label
    while linked[j] != 0:
        j = linked[j]
    return j

def union(label1, label2, linked): #объеденить метки
    j = find(label1, linked)
    k = find(label2, linked)
    if j!=k: #чтобы граф не был зациклен
        linked[k] = j

def two_pass_labeling(B): # сам алгоритм
    linked = np.zeros(B.size // 2, dtype='uint16')
    labeled = np.zeros_like(B, dtype='uint16')
    label = 1
    for row in range(B.shape[0]):
        for col in range(B.shape[1]):
            if B[row, col] != 0:
                lbs = []
                nbs = list(filter(None, neighbours2(B, row, col)))
                for nb in nbs:
                    lbs.append(labeled[nb])
                if not lbs:
                    label += 1
                    m = label
                else:
                    m = min(lbs)
                labeled[row, col] = m
                for nb in nbs:
                    lb = labeled[nb]
                    if lb != m:
                        union(m, lb, linked)
    for row in range(B.shape[0]):
        for col in range(B.shape[1]):
            if B[row, col] != 0:
                new_label = find(labeled[row, col], linked)
                if new_label != labeled[row, col]:
                    labeled[row, col] = new_label
    print(labeled)
    print(linked)

    return labeled            




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

image = two_pass_labeling(image)
plt.imshow(image)
plt.show()
