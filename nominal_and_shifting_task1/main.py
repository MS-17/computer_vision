import numpy as np
import matplotlib.pyplot as plt


def plot_images(images: dict, nrows: int = 1, ncols: int = 1) -> None:
	"""
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


# subtask 1 - get nominal resolution
def subtask1(plot_imgs: bool = False) -> None:
	imgs = {} 
	# imgs is a dict in the following format: {"image_title": {"max_length": int}, {"data": 2Darray}}
	for i in range(1, 7):		
		path = "figure" + str(i) + ".txt"
		imgs[path] = {}
		imgs[path]["max_length"] = int(np.loadtxt(path, max_rows=1))
		imgs[path]["data"] = np.loadtxt(path, skiprows=2)
	
	if plot_imgs:
		plot_images(imgs, 2, 3)

	res = get_nominal_resolution(imgs)
	for title, resolution in res.items():
		print(title, resolution)



def get_transition_vector():
	...


def main():
	subtask1(plot_imgs=False)

	# subtask 2
	get_transition_vector()
	
	return 0


if __name__ == '__main__':
	main()



