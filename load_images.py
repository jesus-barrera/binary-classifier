from PIL import Image
import numpy as np

def Image_To_Npy_Array(image):
	npArray = np.zeros((image.size[0] * image.size[1]))
	pix = image.load()

	for x in range (image.size[0]):
		for y in range (image.size[1]):
			if pix[x, y][0] == 255:
				npArray[(x*image.size[1])] = 1
			else:
				npArray[(x*image.size[1])] = 0

	return npArray

def Binarize_Image(path, threshold):
	img = Image.open(path)
	pix = img.load()

	for x in range (img.size[0]):
		for y in range (img.size[1]):
			if pix[x, y][0] >= threshold:
				pix[x, y] = (255, 255, 255)
			else:
				pix[x, y] = (0, 0, 0)

	#img.show() # Show the binarize new image
	return img

def Load_Image(path):
	threshold = 110 # Default for our test
	img = Binarize_Image(path, threshold)
	return Image_To_Npy_Array(img)

def main():
	path_image = 'Pinguinos.jpg'
	numpy_vector = Load_Image(path_image)	

if __name__ == '__main__':
	main()

