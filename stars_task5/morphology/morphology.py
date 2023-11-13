import matplotlib.pyplot as plt
import numpy as np
from scipy.misc import face


# shift image in the direction of the given vector
def translation(image, vector):
	translated = np.zeros_like(image)
	for i in range(image.shape[0]):
		for j in range(image.shape[1]):
			ni = i - vector[0]
			nj = j - vector[1]
			if ni < 0 or nj < 0:
				continue
			if ni >= image.shape[0] or nj >= image.shape[1]:
				continue
			translated[ni, nj]  = image[i, j]
	return translated


# put mask on an image (наращивание), struct = mask
def dilation(arr, struct):
	result = np.zeros_like(arr)
	for y in range(1, arr.shape[0] - 1):	# skip edges so that not to write checks
		for x in range(1, arr.shape[1] - 1):
			# if arr[y, x] == 0 do nothing, mask is 0. If 1, there is put all ones in the mask
			alog = np.logical_and(arr[y, x], struct)
			# cut mask 3 * 3
			result[y - 1 : y + 2, x - 1 : x + 2] = np.logical_or(result[y - 1 : y + 2, x - 1 : x + 2], alog)
	return result


# delete pixel if the masks doesn't match the area of the image
def erosion(arr, struct):
	result = np.zeros_like(arr)
	for y in range(1, arr.shape[0] - 1):    # skip edges so that not to write checks
		for x in range(1, arr.shape[1] - 1):
			# this won't work with for example crossed mask [010, 111, 010] you need to make logical operators
			sub = arr[y - 1 : y + 2, x - 1 : x + 2]
			if np.all(sub == struct):
				result[y, x] = 1
	return result


def closing(arr, struct):
	return erosion(dilation(arr, struct), struct)


def opening(arr, struct):
	return dilation(erosion(arr, struct), struct)


# you may take those operations from scipy.ndimage

#image = face(gray=True)
#t = translation(image, (20, 50))

arr = np.array([[0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,1,1,1,1,1,1,1,0,0],
                [0,0,0,0,1,1,1,1,0,0],
                [0,0,0,0,1,1,1,1,0,0],
                [0,0,0,1,1,1,1,1,0,0],
                [0,0,0,0,1,1,1,1,0,0],
                [0,0,0,1,1,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0]])

struct = np.ones((3, 3))

plt.subplot(221)
plt.imshow(arr)

plt.subplot(222)
plt.imshow(opening(arr, struct)) #, cmap='gray')

plt.subplot(223)
plt.imshow(closing(arr, struct))
plt.show()
