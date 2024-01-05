import cv2
import threading
import numpy as np
from skimage.metrics import structural_similarity as ssim
from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
from PIL import Image, ImageTk


# Global Variable
inspection_running = False
reference_image_path = None
reference_image = None
inspection_interval = 30
capture_folder = "captures-folder"
capture_interval = 5
captured_image_path = None

# Set a threshold for SSIM value
threshold_value = 0.90  # Change the threshold value as needed

# Tambahkan variabel global untuk menghitung objek Good dan Not Good
good_objects_count = 0
not_good_objects_count = 0

# Fungsi untuk mengubah Threshold
def change_threshold():
    global threshold_value
    new_threshold = simpledialog.askfloat("Change Threshold", "Enter new threshold value (0.00 - 1.00):", minvalue=0, maxvalue=1)
    if new_threshold is not None:
        threshold_value = new_threshold

# Fungsi untuk menghentikan inspeksi
def stop_inspection():
    global inspection_running
    inspection_running = False

# Fungsi untuk memulai inspeksi dalam thread terpisah
def start_inspection_thread():
    thread_inspection = threading.Thread(target=start_inspection)
    thread_inspection.start()
    
# Fungsi untuk mengubah Interval Waktu Inspeksi
def change_inspection_interval():
    global inspection_interval
    new_interval = simpledialog.askinteger("Change Inspection Interval", "Enter new interval (milliseconds):", minvalue=1)
    if new_interval is not None:
        inspection_interval = new_interval

# Fungsi untuk melakukan inspeksi kualitas
def quality_inspection(frame, reference_image):
    global threshold_value, good_objects_count, not_good_objects_count, captured_image_path
    
    if captured_image_path is None:
        return None, None, frame
    
    # Convert both frames to grayscale for SSIM calculation
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_reference = cv2.cvtColor(reference_image, cv2.COLOR_BGR2GRAY)
    
    # Calculate SSIM
    ssim_value = ssim(gray_reference, gray_frame)
    
    # Perform edge detection (using Canny in this example)
    edges_frame = cv2.Canny(gray_frame, 50, 150)
    
    # Find contours in the edge-detected image
    contours, _ = cv2.findContours(edges_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Draw bounding boxes around detected objects
    frame_with_boxes = frame.copy()  # Create a copy of the frame
    
    # Loop through the contours and draw bounding boxes
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame_with_boxes, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Calculate and display the area of the bounding box
        area = w * h
        cv2.putText(frame_with_boxes, f"Area: {area} pixels", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    
    # Determine the result based on SSIM and threshold
    if ssim_value > threshold_value:
        result = "Good"
        good_objects_count += 1
    else:
        result = "Not Good"
        not_good_objects_count += 1
    
    return result, ssim_value, frame_with_boxes

# Fungsi untuk memilih gambar referensi
def register_reference_image():
    global reference_image_path, reference_image

    reference_image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])

    if reference_image_path:
        # Load the reference image and apply chroma keying
        reference_image = cv2.imread(reference_image_path)
        reference_image = cv2.cvtColor(reference_image, cv2.COLOR_BGR2RGB)
        reference_image = Image.fromarray(reference_image)
        reference_image = ImageTk.PhotoImage(reference_image)

        # Display the reference image in the GUI
        reference_panel.configure(image=reference_image)
        reference_panel.image = reference_image

        # Update the global reference image variable
        reference_image = cv2.cvtColor(cv2.imread(reference_image_path), cv2.COLOR_BGR2RGB)

# Fungsi untuk memulai deteksi
def start_inspection():
    global reference_image, cap, inspection_running, good_objects_count, not_good_objects_count
    
    inspection_running = True
    
    # Load gambar referensi
    reference_image = cv2.imread(reference_image_path)
    
    # Buka koneksi ke kamera
    cap = cv2.VideoCapture(0)  # Angka 0 menunjukkan kamera bawaan
    
    while inspection_running:
        # Ambil frame dari kamera
        ret, frame = cap.read()
        if not ret:
            break
        
        # Mendapatkan dimensi dari gambar referensi
        reference_height, reference_width, _ = reference_image.shape
        
        # Resize frame dari kamera agar memiliki dimensi yang sama dengan gambar referensi
        frame = cv2.resize(frame, (reference_width, reference_height))
        
        # Perform quality inspection
        result, ssim_value, frame_with_boxes = quality_inspection(frame, reference_image)
        
        # Tampilkan jumlah objek
        cv2.putText(frame_with_boxes, f"Good: {good_objects_count}", (20, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame_with_boxes, f"Not Good: {not_good_objects_count}", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # Tampilkan hasil inspeksi dengan SSIM value
        cv2.putText(frame_with_boxes, f"Result: {result}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame_with_boxes, f"SSIM: {ssim_value:.2f}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Konversi frame untuk ditampilkan di GUI
        frame_with_boxes_rgb = cv2.cvtColor(frame_with_boxes, cv2.COLOR_BGR2RGB)
        frame_with_boxes_tk = ImageTk.PhotoImage(Image.fromarray(frame_with_boxes_rgb))
        panel.configure(image=frame_with_boxes_tk)
        panel.image = frame_with_boxes_tk
        
        # Jika 'q' ditekan, hentikan loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        cv2.waitKey(inspection_interval)
    
    inspection_running = False
    cap.release()
    cv2.destroyAllWindows()

# Inisialisasi GUI untuk input gambar referensi
root_reference = Tk()
root_reference.title("Input Referensi")

# Frame untuk input gambar referensi
frame_reference = Frame(root_reference, width=400, height=400)
frame_reference.pack()

# Tombol untuk memilih gambar referensi
select_button = Button(frame_reference, text="Select Reference Image", command=register_reference_image)
select_button.pack(pady=10)

# Panel untuk menampilkan gambar referensi
reference_panel = Label(frame_reference)
reference_panel.pack(padx=10, pady=10)

# Inisialisasi GUI untuk proses inspeksi
root_inspection = Toplevel()
root_inspection.title("Proses Inspeksi")

# Frame untuk proses inspeksi
frame_inspection = Frame(root_inspection, width=400, height=400)
frame_inspection.pack()

# Tombol untuk memulai inspeksi
start_button = Button(frame_inspection, text="Start Inspection", command=start_inspection_thread)
start_button.pack(pady=10)

# Tombol untuk menghentikan inspeksi
stop_button = Button(frame_inspection, text="Stop Inspection", command=stop_inspection)
stop_button.pack(pady=10)

# Tombol untuk mengubah threshold
change_threshold_button = Button(frame_inspection, text="Change Threshold", command=change_threshold)
change_threshold_button.pack(pady=10)

change_interval_button = Button(frame_inspection, text="Change Inspection Interval", command=change_inspection_interval)
change_interval_button.pack(pady=10)

# Panel untuk menampilkan frame dengan inspeksi
panel = Label(frame_inspection)
panel.pack(padx=10, pady=10)

# Jalankan kedua GUI
root_reference.mainloop()
root_inspection.mainloop()
