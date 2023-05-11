"""
@author Dan Blanchette
@date May 9th 2023

@description: This program will use k-means clustering via the open CV library to segement microglia cells 
in zebrafish microscopy images. The implmentation will also attempt to remove white noise from each image to help
pre-process the image stack for further analysis. This is imperative as the cells fluro-protiens emit a "lime green"
hue and the color white conflicts with its pixel range for image threshold settings.


@references
1) The Python Code Family of Sites. 
How to Use K-Means Clustering for Image Segmentation using OpenCV in Python, 2023, 
https://www.thepythoncode.com/article/kmeans-for-image-segmentation-opencv-python. 
Accessed 05 May. 2023.

2) Digital Sreeni. Image Segmentation using K-means, 2019, 
https://www.youtube.com/watch?v=6CqRnx6Ic48&t=648s. 
Accessed 05 May. 2023.

3) Dan Blanchette, Dr. Dianna Mitchell PhD, Dr. Seth Long PhD. I
mage segmentation of microglia cells in zebrafish, 2022, 
https://github.com/Dan-Blanchette/INBRE-Internship-2022. 
Accessed 05 May. 2023
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
# import sys

plt.rcParams["figure.figsize"] = (12,50)


def read_image(file_path):
  """Read the images and format to RGB."""
  image = cv2.imread(file_path)
  return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

def preProcessImage(image_name):
  """Reshape the image into a 2D array of pixels and three color channel values (RGB), then convert to float."""
  pixel_val = image_name.reshape((-1,3))
  return np.float32(pixel_val)

def kmeans_clustering(pixel_val, k =3):
  """Apply k means clustering to each of the pixel values."""
  criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
  # last parameter can be adjusted to use PP_CENTERS for centroid calculation if random centers do not yield decent resuts
  compactness, labels, centers = cv2.kmeans(pixel_val, k, None, criteria, 10, cv2.KMEANS_PP_CENTERS)
  return compactness, labels, np.uint8(centers)

def segment_image(image, labels, centers):
  """Segment each image using the cluster centroid(s)."""
  segmentedImage = centers[labels.flatten()]
  return segmentedImage.reshape(image.shape)

def imageMask(image, labels, disabledCluster):
  """Generate a masked image by disabling a defined cluster"""
  maskedImage = np.copy(image).reshape((-1,3))
  maskedImage[labels.flatten() == disabledCluster] = [0,0,0]
  return maskedImage.reshape(image.shape)

def displayImg(image):
  """Display the iamge using matplotlib."""
  plt.imshow(image)
  plt.show()


# MAIN CODE
def main():
  # image_path = sys.argv[1]
  # k = int(sys.argv[2])
  # read the image data
  # image = read_image('image_path')
  
  # fig, ax = plt.subplots(6, 2, sharey=True)
  
  for i in range(1, 40):
    image = read_image(str(i) + '.png')
    #  image = read_image('1.png')
    # pre-process the image
    K = 5
    pixel_val = preProcessImage(image)

    compactness, labels, centers = kmeans_clustering(pixel_val, K)

    segmented_img = segment_image(image, labels, centers)

     # displayImg(segmented_img)
     # ax[i, 1].imshow(segmented_img)
     # ax[i, 1].set_title('K = %s Image'%K)
     # ax[i, 0].imshow(image)
     # ax[i, 0].set_title('Original Image')
    
    cv2.imwrite('results1/kmeans_seg_' + str(i) + '.png', segmented_img)

    cluster_to_black = 2

    masked_image = imageMask(image, labels, cluster_to_black)

     # displayImg(masked_image)
    
     # ax[i, 1].imshow(masked_image)
     # ax[i, 1].set_title('K-means With Mask')
     # ax[i, 0].imshow(image)
     # ax[i, 0].set_title('Original Image')
    
    cv2.imwrite('results2/kmeans_mask_' + str(i) + '.png', masked_image)
    
    print("now processing image: ", i)

    

if (__name__ == '__main__'):
  main()