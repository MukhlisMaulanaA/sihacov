import cv2
from cv2 import cuda

print(cv2.getBuildInformation())

cuda.printCudaDeviceInfo(0)