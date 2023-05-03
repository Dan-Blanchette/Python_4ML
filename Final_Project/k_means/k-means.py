import numpy as np
import matplotlib.pyplot as plt
import cv2


image = cv2.imread('../pngimgs/2.png')

image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

plt.imshow(image)

# print("Hello World!")