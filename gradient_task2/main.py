import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import rotate


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


# the first approach to get the diagonal gradient (with swapaxes)
def get_diagonal_grad_first(img, color1, color2):
	image = img.copy()
	image = np.swapaxes(image, 0, 2)
	# print(image.shape)
	
	# I need 199 values 
	# like if we want to fill 3*3 matrix we'll do:
	# [[1, 2, 3,], [2, 3, 4], [3, 4, 5]] so that the values are distributed on the diagonals
	# the total number of diagonals in a square matrix is 2 * shape[0] - 1, so we need in case of 3 * 3 5 values
	ratios = np.linspace(0, 1, 2 * image.shape[1] - 1)	

	vals = []
	for i, t in enumerate(ratios):
		r = lerp(color1[0], color2[0], t)
		g = lerp(color1[1], color2[1], t)
		b = lerp(color1[2], color2[2], t)
		vals.append([r, g, b])

	for i in range(image.shape[1]):

		# interesting effect 
		# image[:, i, :] = vals[i:img.shape[1] + i]

		image[:, i, :] = np.array(vals[i:img.shape[1] + i]).T
	
	return np.swapaxes(image, 0, 2)


# the second approach to get the diagonal gradient (without swapaxes)
def get_diagonal_grad_second(img, color1, color2):
	image = img.copy()

	ratios = np.linspace(0, 1, 2 * image.shape[1] - 1)	

	vals = []
	for i, t in enumerate(ratios):
		r = lerp(color1[0], color2[0], t)
		g = lerp(color1[1], color2[1], t)
		b = lerp(color1[2], color2[2], t)
		vals.append([r, g, b])

	for i in range(image.shape[0]):
		image[i, :, :] = vals[i : image.shape[0] + i]
	return image


def main():

	size = 100
	# 100 * 100 * 3. [255, 128, 0] * 100 will be just one layer (in case of vertical gradient)
	# and there will be 100 such layers with different colors. Each layers is in fact a row 
	# in a final image
	image = np.zeros((size, size, 3), dtype="uint8")	

	color1 = [255, 128, 0]
	color2 = [0, 128, 255]
	# color1 = [114, 18, 24]
	# color2 = [2, 195, 250]

	image = get_vertical_grad(image, color1, color2)
	im1 = get_diagonal_grad_first(image, color1, color2)
	im2 = get_diagonal_grad_second(image, color1, color2)
	
	# print(image)
	# print(np.swapaxes(im1, 0, 2))
	# print(np.swapaxes(im2, 0, 2))

	imgs = {"Vertical": {"data": image}, "Diagonal1": {"data": im1}, "Diagonal2": {"data": im2}}
	plot_images(imgs, 1, 3)
	return 0


if __name__ == '__main__':
	main()
