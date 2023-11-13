import numpy as np
import matplotlib.pyplot as plt


def negate(B):
    return B.copy() * -1


def neighbours4(y, x):
    return (y, x+1), (y, x-1), (y-1, x), (y+1, x)


def neighbours8(y, x):
     return neighbours4(y, x) + ((y-1, x+1), (y+1, x+1), (y-1, x-1), (y+1, x-1))


def search(LB, label, y, x, connectivity=neighbours4):
    LB[y, x] = label
    for ny, nx in connectivity(y, x):
        if LB[ny, nx]== -1:
            search(LB, label, ny, nx)


def recursive_labeling(B):
    LB = negate(B)
    label = 0
    for y in range(LB.shape[0]):
        for x in range(LB.shape[1]):
            if LB[y, x] == -1:
                label += 1
                search(LB, label, y, x, neighbours8)

    return LB


#
# the same as recursive algorithm above but without recursion (algo "two pass")
#

# y is rows and x is columns
# check if a point (y,x) can be a neighbour
def check(B, y, x):
	"""
	if not 0 <= y < B.shape[0]:
		return False
	if not 0 <= x < B.shape[1]:
		return False
	if B[y, x] != 0:
		return True
	return False
	"""
	# or simply:
	return x >= 0 and y >= 0 and B[y,x]

def neighbours2(B, y, x):
	left_nb = y, x - 1
	top_nb = y - 1, x
	# check if neighbours exist, if not assign None
	if not check(B, *left_nb):
		left_nb = None
	if not check(B, *top_nb):
		top_nb = None
	return left_nb, top_nb


# creates graph 'linked'. Initially linked is a zero array
# if label1 = 6, label2 = 8 then linked = [0, 0, 0, 0, 0, 0, 0, 0, 6]
# (that means that 8 is connected with 6)
def union(label1, label2, linked):
	j = find(label1, linked)
	k = find(label2, linked)
	if j != k:
		linked[k] = j

	#return linked


# find the minimal label in the graph "linked"
def find(label, linked):
	j = label
	while linked[j] != 0:
		j = linked[j]
	return j


def two_pass_labelling(B):
	# on a chess board each cell doesn't have a top and a left neighbour of the same color
	# that's why the number of black cells is the approximate number of
	# elements in our graph 'linked'. That's why we count it as B.size / 2
	# where B.size is the number of elements on the board
	linked = np.zeros(B.size // 2, dtype="uint16")
	labelled = np.zeros_like(B, dtype="uint16")

	label = 1
	for row in range(B.shape[0]):
		for col in range(B.shape[1]):
			if B[row, col] != 0:
				labels = []
				nbs = list(filter(None, neighbours2(B, row, col)))
				print(f"Nbs for {[row, col]}: {nbs}")
				for nb in nbs:
					labels.append(labelled[nb])
				# if both neighbours are None, create new label
				if not labels:
					label += 1
					m = label
				else:
					m = min(labels)
				labelled[row, col] = m

				# create graph, mark which label is connected to which label
				for nb in nbs:
					label = labelled[nb]
					if label != m:
						union(m, label, linked)
	#print(linked)


	# make second iteration of the algorithm to draw figures in one color

	for row in range(B.shape[0]):
		for col in range(B.shape[1]):
			if B[row, col] != 0:
				new_label = find(labelled[row, col], linked)
				if new_label != labelled[row, col]:
				    labelled[row, col] = new_label
	print(linked)
	print(labelled)
	return labelled


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

image = two_pass_labelling(image)
#image = recursive_labeling(image)
plt.imshow(image)
plt.show()
