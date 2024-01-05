import cv2
from skimage.metrics import structural_similarity as ssim

# Fungsi untuk melakukan inspeksi kualitas
def quality_inspection(frame, reference_image):
    # Convert both frames to grayscale for SSIM calculation
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_reference = cv2.cvtColor(reference_image, cv2.COLOR_BGR2GRAY)
    
    # Calculate SSIM
    ssim_value = ssim(gray_reference, gray_frame)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    blurred = cv2.GaussianBlur(gray_frame, (5, 5), 0)
    
    blurred2 = cv2.GaussianBlur(reference_image, (5, 5), 0)
    
    # Perform edge detection (using Canny in this example)
    edges_frame = cv2.Canny(blurred, 50, 10)
    
    edges_frame2 = cv2.Canny(blurred2, 50, 10)
    
    dilate = cv2.dilate(edges_frame, kernel, iterations=1)
    
    dilate2 = cv2.dilate(edges_frame2, kernel, iterations=1)
    
    # Find contours in the edge-detected image
    contours, _ = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    contours2, _ = cv2.findContours(dilate2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
    
    # Draw bounding boxes around detected objects
    frame_with_boxes = frame.copy()  # Create a copy of the frame
    cv2.drawContours(frame_with_boxes, contours, -1, (0, 255, 0), 2)
    
    frame_with_reference = reference_image.copy()
    cv2.drawContours(frame_with_reference, contours2, -1, (0, 255, 0), 2)
    
    # frame_with_video = gray_frame.copy()
    # cv2.drawContours(frame_with_video, contours, -1, (0, 255, 0), 0)
    
    # Set a threshold for SSIM value
    threshold = 0.97  # Change the threshold value as needed
    
    # Determine the result based on SSIM and threshold
    if ssim_value > threshold:
        result = "Good"
    else:
        result = "Not Good"
    
    return result, ssim_value, frame_with_boxes, frame_with_reference

# Fungsi untuk melakukan resize pada gambar
def resize_image(image, new_width, new_height):
    return cv2.resize(image, (new_width, new_height))

# Load gambar referensi
reference_image = cv2.imread('jarum-suntik.jpg')  # Ganti dengan gambar referensi Anda

# url = "http://192.168.43.138:4747/video"

# Buka koneksi ke kamera
cap = cv2.VideoCapture("test2.mp4")  # Angka 0 menunjukkan kamera bawaan

# Loop utama untuk memproses frame secara real-time
while True:
    # Ambil frame dari kamera
    ret, frame = cap.read()
    if not ret:
        break
    
    # Mendapatkan dimensi dari gambar referensi
    reference_height, reference_width, _ = reference_image.shape
    
    # Resize frame dari kamera agar memiliki dimensi yang sama dengan gambar referensi
    frame = resize_image(frame, reference_width, reference_height)
    
    # Perform quality inspection
    result, ssim_value, frame_with_boxes, frame_with_reference = quality_inspection(frame, reference_image)
    
    # Tampilkan hasil inspeksi dengan SSIM value
    if result == "Good":
      cv2.putText(frame_with_boxes, f"Result: {result}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    else:
      cv2.putText(frame_with_boxes, f"Result: {result}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(frame_with_boxes, f"SSIM: {ssim_value:.2f}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # Tampilkan frame dengan inspeksi
    cv2.imshow('Quality Inspection', frame_with_boxes)
    cv2.imshow('Reference Image', frame_with_reference)
    
    # Jika 'q' ditekan, hentikan loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Bebaskan sumber daya dan tutup jendela
cap.release()
cv2.destroyAllWindows()
