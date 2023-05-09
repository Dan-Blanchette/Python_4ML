import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys

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
  # last parameter can be adjusted to use PP_CENTERS for centroid calculation if random centers do no yield decent resuts
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
  k = 5
  # read the image data
  # image = read_image('image_path')

  for i in range(1, 40):
    image = read_image( str(i) + '.png')

  # pre-process the image

    pixel_val = preProcessImage(image)

    compactness, labels, centers = kmeans_clustering(pixel_val, k)

    segmented_img = segment_image(image, labels, centers)

    displayImg(segmented_img)
    
    cv2.imwrite('kmeans_seg_' + str(i) + '.png', segmented_img)

    cluster_to_black = 2

    masked_image = imageMask(image, labels, cluster_to_black)

    displayImg(masked_image)
    
    cv2.imwrite('kmeans_mask_' + str(i) + '.png', masked_image)
    
    print("now processing image: ", i)
    

if (__name__ == '__main__'):
  main()