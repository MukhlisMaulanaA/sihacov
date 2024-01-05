import cv2
import numpy as np

cap = cv2.VideoCapture("./test2.mp4") 

while True:
  
  # Baca frame dari webcam
  ret, frame = cap.read()

  # Konversi ke grayscale
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

  # Threshold untuk mendapatkan efek biner    
  ret, th = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY)

  # Tampilkan frame asli dan frame threshold
  cv2.imshow('Webcam', frame)
  cv2.imshow('Webcam Threshold', th)

  # Berhenti jika tombol 'q' ditekan
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

# Tutup semua jendela    
cv2.destroyAllWindows()
cap.release()