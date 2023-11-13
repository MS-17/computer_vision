import numpy as np
import matplotlib.pyplot as plt


def plot_images(images: dict, nrows: int = 1, ncols: int = 1) -> None:
	"""
		images: <title: <data: image>> dictionary
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


def get_nominal_resolution(plot_imgs: bool = True):
	imgs = {} 
	for i in range(1, 7):		
		path = "figure" + str(i) + ".txt"
		imgs[path] = {}
		imgs[path]["max_length"] = int(np.loadtxt(path, max_rows=1))
		imgs[path]["data"] = np.loadtxt(path, skiprows=2)
	
	# print(imgs)
	if plot_imgs:
		plot_images(imgs, 2, 3)

	img1 = imgs["figure1.txt"]["data"]
	print(img1 == 1)

	# todo find the longest row that contains ones

	# plt.imshow(imgs["figure6.txt"]["data"])
	# plt.show()


def get_transition_vector():
	...


def main():
	# subtask 1
	get_nominal_resolution(False)

	# subtask 2
	get_transition_vector()
	
	return 0


if __name__ == '__main__':
	main()



