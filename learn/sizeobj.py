import cv2

# Buka webcam 
cap = cv2.VideoCapture("./test2.mp4")

# Inisialisasi ID dan status untuk setiap titik
points = []
point_id_counter = 1

while True:
    # Baca frame
    ret, frame = cap.read()
    
    # Tambahkan garis tengah pada tampilan GUI
    cv2.line(frame, (frame.shape[1] // 2, 0), (frame.shape[1] // 2, frame.shape[0]), (0, 255, 255), 2)
    
    # Konversi ke grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Deteksi tepi 
    edges = cv2.Canny(blurred, 50, 100)
    
    dilate = cv2.dilate(edges, kernel, iterations=1)
    
    # Cari kontur 
    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2:]
    
    # Iterasi tiap kontur
    for cnt in contours:
        
        # Hitung luas kontur 
        area = cv2.contourArea(cnt)
        
        # Dapatkan bounding box
        x, y, w, h = cv2.boundingRect(cnt)
        
        # Hitung titik pusat
        center_x = x + w // 2
        center_y = y + h // 2
        
        # Gambar kotak bounding box 
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Tampilkan teks ukuran dan koordinat pusat
        cv2.putText(frame, f"{w}x{h} cm", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Center: ({center_x}, {center_y})", (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        
        # Gambar titik pusat
        cv2.circle(frame, (center_x, center_y), 5, (255, 0, 0), -1)
        
        # Cek apakah titik pusat berada tepat di garis tengah
        line_x = frame.shape[1] // 2
        
        if center_y == line_x:
            # Cek apakah titik tersebut sudah terdeteksi sebelumnya
            point_exists = False
            for point in points:
                if point['id'] == point_id_counter:
                    point_exists = True
                    break
            
            # Jika belum terdeteksi, tambahkan titik ke daftar dan simpan screenshot
            if not point_exists:
                points.append({'id': point_id_counter, 'coordinates': (center_x, center_y)})
                point_id_counter += 1
                cv2.imwrite(f"captures-folder/screenshot_id_{point_id_counter}.jpg", frame)
    
    # Tampilkan ID setiap titik
    for point in points:
        cv2.putText(frame, f"ID: {point['id']}", point['coordinates'], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
    # Tampilkan hasil 
    cv2.imshow('Estimasi Ukuran', frame)
    
    if cv2.waitKey(1) == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()
