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
threshold_value = 0.99
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
    thread = threading.Thread(target=start_inspection)
    thread.start()

# Fungsi untuk melakukan inspeksi kualitas
def quality_inspection(frame, reference_image):
    global threshold_value, good_objects_count, not_good_objects_count
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
    cv2.drawContours(frame_with_boxes, contours, -1, (0, 255, 0), 2)

    # Determine the result based on SSIM and threshold
    if ssim_value > threshold_value:
        result = "Good"
        good_objects_count += 1
    else:
        result = "Not Good"
        not_good_objects_count += 1

    return result, ssim_value, frame_with_boxes

# Fungsi untuk memilih gambar referensi
def select_reference_image():
    global reference_image_path, reference_image
    reference_image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])
    reference_image = cv2.imread(reference_image_path)
    reference_image = cv2.cvtColor(reference_image, cv2.COLOR_BGR2RGB)
    
    update_reference_image()

# Fungsi untuk memulai deteksi
def start_inspection():
    global reference_image, cap, inspection_running, good_objects_count, not_good_objects_count

    inspection_running = True
    
    reference_image = cv2.imread(reference_image_path)

    # Buka koneksi ke kamera
    cap = cv2.VideoCapture("test2.mp4")  # Angka 0 menunjukkan kamera bawaan

    # Loop utama untuk memproses frame secara real-time
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
        cv2.putText(frame_with_boxes, f"Good: {good_objects_count}", (20, 400), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 255, 0), 2)
        cv2.putText(frame_with_boxes, f"Not Good: {not_good_objects_count}", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 0, 255), 2)

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

    inspection_running = False
    cap.release()
    cv2.destroyAllWindows()

# Fungsi untuk memperbarui gambar referensi di GUI
def update_reference_image():
    global reference_image

    # Tampilkan gambar referensi di GUI
    reference_image = cv2.cvtColor(reference_image, cv2.COLOR_BGR2RGB)
    reference_image = Image.fromarray(reference_image)
    reference_image_tk = ImageTk.PhotoImage(reference_image)
    reference_panel.configure(image=reference_image_tk)
    reference_panel.image = reference_image_tk

# Inisialisasi GUI untuk input gambar referensi
root_reference = Tk()
root_reference.title("Input Referensi")

# Frame untuk input gambar referensi
frame_reference = Frame(root_reference, width=400, height=400)
frame_reference.pack()

# Tombol untuk memilih gambar referensi
select_button = Button(frame_reference, text="Select Reference Image", command=select_reference_image)
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

# Panel untuk menampilkan frame dengan inspeksi
panel = Label(frame_inspection)
panel.pack(padx=10, pady=10)

# Jalankan kedua GUI
root_reference.mainloop()
root_inspection.mainloop()
