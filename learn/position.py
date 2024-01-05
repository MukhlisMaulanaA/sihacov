import cv2
import numpy as np

# Fungsi untuk mendeteksi objek pada frame
def detect_object(frame, lower_color, upper_color):
    # Konversi frame ke format HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Definisikan batas warna objek
    lower = np.array(lower_color, dtype=np.uint8)
    upper = np.array(upper_color, dtype=np.uint8)

    # Buat mask untuk objek berdasarkan batas warna
    mask = cv2.inRange(hsv, lower, upper)

    # Temukan kontur pada mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Jika terdapat kontur, hitung pusat objek
    if contours:
        # Ambil kontur terbesar (asumsi objek utama)
        largest_contour = max(contours, key=cv2.contourArea)
        moments = cv2.moments(largest_contour)

        # Hitung pusat objek
        if moments["m00"] != 0:
            cx = int(moments["m10"] / moments["m00"])
            cy = int(moments["m01"] / moments["m00"])

            # Tampilkan pusat objek pada frame
            cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)
            cv2.putText(frame, f"Center: ({cx}, {cy})", (cx - 50, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

# Inisialisasi webcam
cap = cv2.VideoCapture("test2.mp4")

# Range warna objek (contoh: warna biru)
lower_blue = [150, 150, 150]
upper_blue = [196, 95, 0]

while True:
    # Baca frame dari webcam
    ret, frame = cap.read()

    # Deteksi objek pada frame
    detect_object(frame, lower_blue, upper_blue)

    # Tampilkan frame
    cv2.imshow("Object Detection", frame)

    # Hentikan program jika tombol 'q' ditekan
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Lepaskan sumber daya
cap.release()
cv2.destroyAllWindows()
