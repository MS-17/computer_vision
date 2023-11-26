import numpy as np
import matplotlib.pyplot as plt



# predicts v[x, y] between v0=[x0, y0] and v1=[x1, y1], t is a ratio
#
# for ex if t=0.2 it means that we want some point x
# between x0 and x1 which is 20% farther from x0 (and the same for y at the same time)
#
# it gets x with x0 + (x1 - x0) * t (which is basically a distance between x0 and x1 multiplied by
# the ratio t and then summed with x0)
#
# let's assume v0 = [1, 2] and v1 = [4, 4]
# then 
# (4 - 1) * 0.2 = 0.6 is how far x is from x0 and then x0 + 0.6 = 1 + 0.6 = 1.6
# for y: (4 - 2) * 0.2 = 0.4 and then 2 + 0.4 = 2.4
#
# in the function below we have v0 + t * (v1 - v0) but in other form:
# v0 + t(v1 - v0) = v0 + t * v1 - t * v0 = (1 - t) * v0 + t * v1
def lerp(v0, v1, t):
	return (1 - t) * v0 + t * v1


# from top to bottom
def get_vertical_grad(img, color1, color2):
	image = img.copy()
	ratios = np.linspace(0, 1, image.shape[0])
	# generate all points for each given ratio ("ratios" array) between color1 red and color2 red 
	# (and do the same for the green and blue)
	# walking with lerp 255 => 0 in case of red, 128 => 128 in case of green
	# and 0 => 255 in case of blue we create an effect of smooth color transition 
	# (when we combine r+g+b (their new values) in one pixel)
	for i, t in enumerate(ratios):
		r = lerp(color1[0], color2[0], t)
		g = lerp(color1[1], color2[1], t)
		b = lerp(color1[2], color2[2], t)
		# fill i row with r+g+b color
		image[i, :, :] = [r, g, b]
	return image
from scipy.ndimage import rotate

def get_diagonal_grad(img, color1, color2):
	image = img.copy()
	# image = np.swapaxes(image, 0, 2)
	print(image.shape)

	ratios = np.linspace(0, 1, image.shape[1])
	for i, t in enumerate(ratios):
		r = lerp(color1[0], color2[0], t)
		g = lerp(color1[1], color2[1], t)
		b = lerp(color1[2], color2[2], t)

		# todo complete
		for j in range(i, -1, -1):
			print(j)
			for k in range(image.shape[1]):
				image[:, j, k] = [r, g, b]

		# for 

		# image[i, :, :] = [r, g, b]
	return np.swapaxes(image, 0, 2)


def main():

	size = 100
	# 100 * 100 * 3 [255, 128, 0] * 100 is just one layer and there're 100 such layers with 
	# different colors. Each layers is in fact a row in a final image
	image = np.zeros((size, size, 3), dtype="uint8")	
	color1 = [255, 128, 0]
	color2 = [0, 128, 255]
	image = get_vertical_grad(image, color1, color2)
	# image = get_diagonal_grad(image, color1, color2)
	
	# plt.imshow(image)
	# plt.show()


	# the total amount of diagonals in the square matrix is shape[0] * 2 - 1
	
	
	a = np.array([ [[1, 2, 3,], [4, 5, 6,]],  [[7, 8, 9,], [10, 11, 12]] ])
	# print(a.shape)
	# print(a)
	# print(np.swapaxes(a, 0, 2))
	# print(a[:, 0, 1])
	# a = np.flipud(a)
	# np.diagonal(a, offset=0)[:] = [0, 0, 0]
	print(a)
	print(np.diagonal(a, offset=0))



	return 0


if __name__ == '__main__':
	main()






# may be useful
def plot_images(images: dict, nrows: int = 1, ncols: int = 1) -> None:
	"""
		Description: 
			plot multiple images in a single window
		Parameters:
			images: {"image_title": {"data": 2Darray}}
			nrows: a number of rows the window
			ncols: a number of columns in the window
	"""

	if nrows <= 0 or ncols <= 0:
		raise ValueError("nrows or ncols should be greater than 0")

	fig, axes = plt.subplots(nrows=nrows, ncols=ncols)

	if nrows == 1 and ncols == 1:
		axes = [axes]
	elif nrows != 1:
		# axes.ravel() flattens the 2D array of axes 
		axes = axes.ravel()

	for idx, title in enumerate(images):
		if idx + 1 > nrows * ncols:
			break
		# get the current axis via its index
		axis = axes[idx]
		# display a picture in the axis and set picture's title
		axis.imshow(images[title]["data"])
		axis.set_title(title)
		# axis.set_axis_off()

	plt.show()


def get_nominal_resolution(images: dict) -> dict:
	"""
		image: {"image_title": {"max_length": int}, {"data": 2Darray}}
	"""
	result = {}
	for image in images:
		data = images[image]["data"]
		# find the longest row that contains ones and count the nominal resolution	
		sums = data.sum(axis=1)
		max_pixel_length = max(sums)
		nominal_resolution = 0
		if max_pixel_length != 0:
			nominal_resolution = images[image]["max_length"] / max_pixel_length
		result[image] = nominal_resolution
	return result


def subtask1(plot_imgs: bool = False) -> None:
	# imgs is a dict in the following format: {"image_title": {"max_length": int}, {"data": 2Darray}}
	imgs = {} 
	for i in range(1, 7):		
		path = "data/figure" + str(i) + ".txt"
		imgs[path] = {}
		imgs[path]["max_length"] = int(np.loadtxt(path, max_rows=1))
		imgs[path]["data"] = np.loadtxt(path, skiprows=2)
	
	if plot_imgs:
		plot_images(imgs, 2, 3)

	res = get_nominal_resolution(imgs)
	for title, resolution in res.items():
		print(title, resolution)


def get_transition_vector(images: dict) -> list:
	result = []

	t  = list(images.keys())
	im1, im2 = images[t[0]]["data"], images[t[1]]["data"]
	
	# get coordinates of all pixels = 1
	a = np.where(im1 == 1)
	b = np.where(im2 == 1)

	# create matrices of these coordinates
	coords1 = np.column_stack((a[0], a[1]))
	coords2 = np.column_stack((b[0], b[1]))
	
	#subtract the matrices and find the transition vector
	result = np.unique(coords2 - coords1)
	return result


def subtask2(plot_imgs: bool = False) -> None:
	# imgs is a dict in the following format: {"image_title": {"max_length": int}, {"data": 2Darray}}
	imgs = {}
	for i in range(1, 3):		
		path = "data/img" + str(i) + ".txt"
		imgs[path] = {}
		imgs[path]["data"] = np.loadtxt(path, skiprows=2)
	
	if plot_imgs:
		plot_images(imgs, 1, 2)

	res = get_transition_vector(imgs)
	print(f"Transition vector: ({res[0]}, {res[1]})")



