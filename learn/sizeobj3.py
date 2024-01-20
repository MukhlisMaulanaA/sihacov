import cv2

# Faktor konversi dari piksel ke sentimeter
faktor_konversi = 0.1
area_cm_fix = 160.00
counter = 0

# Buka webcam
cap = cv2.VideoCapture("./test2.mp4")

# Tambahkan variabel untuk melacak mode capture
capture_mode = False

while True:
    # Baca frame
    ret, frame = cap.read()

    # Konversi ke grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Deteksi tepi
    edges = cv2.Canny(blurred, 50, 100)

    dilate = cv2.dilate(edges, kernel, iterations=1)

    # Cari kontur
    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Iterasi tiap kontur
    for cnt in contours:
        # Hitung luas kontur
        area_px = cv2.contourArea(cnt)

        # Dapatkan bounding box
        x, y, w, h = cv2.boundingRect(cnt)

        # Hitung titik pusat
        center_x = x + w // 2
        center_y = y + h // 2

        # Hitung luas dalam sentimeter persegi
        area_cm = area_px * faktor_konversi * faktor_konversi

        # Gambar kotak bounding box jika tidak dalam mode "capture"
        if not capture_mode:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Tampilkan teks luas jika tidak dalam mode "capture"
            cv2.putText(frame, f"Luas: {area_cm:.2f} cm^2", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        if area_cm <= area_cm_fix:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, f"Not Good", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"Good", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Gambar titik pusat
        cv2.circle(frame, (center_x, center_y), 5, (255, 0, 0), -1)

    # Tampilkan hasil
    cv2.imshow('Estimasi Luas', frame)

    # Tambahkan logika capture frame jika tombol spasi ditekan
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord(' '):
        capture_mode = not capture_mode
        if capture_mode:
            print("Capture mode ON") 
            counter += 1
            filename = f'capture_id_{counter}.jpg'
            cv2.imwrite(f"captures-folder/{filename}", frame)
        else:
            print("Capture mode OFF")

cap.release()
cv2.destroyAllWindows()
