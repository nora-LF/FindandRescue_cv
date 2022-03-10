# import the necessary packages
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", type=str, required=True,
	help="path to input directory of images to stitch")
ap.add_argument("-o", "--output", type=str, required=True,
	help="path to the output image")
args = vars(ap.parse_args())

dim=(1300,700)
def center_crop(img,dim):
	w, h = img.shape[1], img.shape[0]
	crop_w=dim[0] if dim[0]<img.shape[1] else img.shape[1]
	crop_h=dim[1] if dim[1]<img.shape[0] else img.shape[0]
	mid_x, mid_y = int(w/2), int(h/2)
	cw2, ch2=int(crop_w/2), int(crop_h/2)
	crop_img=img[mid_y-ch2:mid_y+ch2, mid_x-cw2:mid_x+cw2]
	return crop_img


# grab the paths to the input images and initialize our images list
print("[INFO] loading images...")
imagePaths = list(paths.list_images(args["images"]))
images = []

# loop over the image paths, load each one, and add them to our
# images to stich list
for imagePath in imagePaths:
	image = cv2.imread(imagePath)
	#mask=cv2.imread("mask.png")
	#image=cv2.bitwise_and(image, mask)
	images.append(image)

#images=[]

# for image in images_all:
# 	img=cv2.imread(image)
# 	mask=cv2.imread("mask.png").astype("float32")
# 	image=cv2.bitwise_and(image, image, mask=mask)
# 	images.append(image)


# initialize OpenCV's image sticher object and then perform the image
# stitching
print("[INFO] stitching images...")
stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()
(status, stitched) = stitcher.stitch(images)

# turn on when cropping
#stitched=center_crop(stitched, dim)


# if the status is '0', then OpenCV successfully performed image
# stitching
if status == 0:
	# write the output stitched image to disk
	cv2.imwrite(args["output"], stitched)

	# display the output stitched image to our screen
	#cv2.imshow("Stitched", stitched)
	#cv2.waitKey(0)

# otherwise the stitching failed, likely due to not enough keypoints)
# being detected
else:
	print("[INFO] image stitching failed ({})".format(status))



