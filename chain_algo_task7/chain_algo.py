import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label
from collections import Counter
from skimage.filters import threshold_otsu, threshold_li, threshold_local
from skimage.util import view_as_windows


# chain algo

# from the top clockwise
def neighbours4(y, x):
	return (y-1, x), (y, x+1), (y+1, x), (y, x-1)


# from the top clockwise
def neighbours8(y, x):
	return ((y-1, x), (y-1, x+1), (y, x+1), (y+1, x+1), (y+1, x), (y+1, x-1),
			(y, x-1), (y-1, x-1))


def get_bounds(labelled, label=1, connectivity=neighbours8):
	pos = np.where(labelled == label)
	bounds = []
	for y, x in zip(*pos):
		for yn, xn in connectivity(y, x):
			# if on edge of the whole image
			if yn < 0 or yn > labelled.shape[0] - 1:
				bounds.append((y, x))
				break
			elif xn < 0 or xn > labelled.shape[1] - 1:
				bounds.append((y, x))
				break
			elif labelled[yn, xn] == 0:
				bounds.append((y, x))
				break
	return bounds


def chain_algo(labelled, label=1, connectivity=neighbours8):
	result = []
	# vector = {(y, x): value} (we get the directions counterclockwise from the right)
	vectors = {(0, 1): 0, (-1, 1): 1, (-1, 0): 2, (-1, -1): 3, (0, -1): 4, (1, -1): 5, (1, 0): 6, (1, 1): 7}
	bounds = np.array(get_bounds(labelled, label, connectivity))
	# print(bounds)
	
	y_bound = bounds[:, 0]
	x_bound = bounds[:, 1]
	# print(len(bounds))
	
	# get the first point 
	y = bounds[0][0]
	x = bounds[0][1]
	print(f"The first point: {(y, x)}")

	current_direction = None
	previous_direction = None

	for i in range(len(bounds)):

		print(f"Current (y, x): {(y, x)}")

		nbs = connectivity(y, x)
		for nb in nbs:
			if labelled[nb[0], nb[1]] == 1:
				y_ = nb[0] - y
				x_ = nb[1] - x
				result.append(vectors[y_, x_])
				x += x_
				y += y_
				break


	# # starting point
	# x = x_bound[0]
	# y = y_bound[0]
	# current_direction = None

	# # accidentally I made it go counterclockwise
	# for i in range(1, len(x_bound)):
	# 	print("\n", i)
	# 	print("x", x, "y", y)
	# 	print("direction", current_direction)

	# 	previous_direction = current_direction
	# 	count = 0
	# 	nbs = connectivity(y, x)
	# 	print(nbs)
	# 	print(nbs[-1::-1])
	# 	print()
	# 	for yn, xn in nbs[::-1]:
	# 		count += 1
	# 		if labelled[yn, xn] == 1:
	# 			print("x", x, "xn", xn)
	# 			print("y", y, "yn", yn)
	# 			print(labelled[yn, xn])
	# 			print()
	# 			x_ = xn - x
	# 			y_ = yn - y
	# 			current_direction = vectors[(y_, x_)]
	# 			if previous_direction != current_direction:
	# 				continue
	# 			res.append(current_direction)
	# 			x = xn
	# 			y = yn
	# 			break
	# 	print("Iterations:", count)
	return result


# image = np.load("similar.npy")

image = np.loadtxt("ex.dat")

labelled = label(image)
# print(labelled[90:110, 195:210])
labels = np.unique(labelled)[1:]
# print(labels)

bd = np.array(get_bounds(labelled, label=1))
# print(bd)
x_bound = bd[:, 1]
y_bound = bd[:, 0]


# print(chain_algo(labelled))


plt.imshow(labelled)
plt.scatter(x_bound, y_bound)
plt.show()

