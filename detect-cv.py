import cv2
import numpy as np

# Baca gambar
image = cv2.imread('img/angsa.jpg', 0)  # Baca dalam skala abu-abu

# Terapkan filter Gaussian untuk mengurangi noise
blurred = cv2.GaussianBlur(image, (5, 5), 0)

# Terapkan Canny Edge Detection
edges = cv2.Canny(blurred, 50, 100)

# Tampilkan gambar hasil
cv2.imshow('Canny Edge Detection', edges)
cv2.waitKey(0)
cv2.destroyAllWindows()
