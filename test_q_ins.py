import cv2
from skimage.metrics import structural_similarity as ssim
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog


def load_reference_image():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Ask the user to select a reference image
    file_path = filedialog.askopenfilename(title="Select Reference Image", filetypes=[("Image Files", "*.png *.jpg *.jpeg")])

    if file_path:
        reference_image = cv2.imread(file_path)
        return reference_image
    else:
        return None

def load_inspection_image():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Ask the user to select an image for inspection
    file_path = filedialog.askopenfilename(title="Select Image for Inspection", filetypes=[("Image Files", "*.png *.jpg *.jpeg")])

    if file_path:
        inspection_image = cv2.imread(file_path)
        return inspection_image
    else:
        return None

def quality_inspection(frame, reference_image):
    # Function to perform quality inspection
    
    # Convert both frames to grayscale for SSIM calculation
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_reference = cv2.cvtColor(reference_image, cv2.COLOR_BGR2GRAY)
    
    # Calculate SSIM
    ssim_value = ssim(gray_reference, gray_frame)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    blurred = cv2.GaussianBlur(gray_frame, (5, 5), 0)
    
    # Perform edge detection (using Canny in this example)
    edges_frame = cv2.Canny(blurred, 10, 200)
    
    dilate = cv2.dilate(edges_frame, kernel, iterations=1)
    
    # Find contours in the edge-detected image
    contours, _ = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw bounding boxes around detected objects
    frame_with_boxes = frame.copy()  # Create a copy of the frame
    cv2.drawContours(frame_with_boxes, contours, -1, (0, 255, 0), 2)
        
    # Set a threshold for SSIM value
    threshold = 0.98  # Change the threshold value as needed
    
    # Determine the result based on SSIM and threshold
    if ssim_value > threshold:
        result = "Good"
    else:
        result = "Not Good"
    
    return result, ssim_value, frame_with_boxes

# Load initial reference image
reference_image = load_reference_image()

# Jika gambar referensi dimuat dengan sukses, lanjutkan
if reference_image is not None:
    # Buat jendela Tkinter
    root = tk.Tk()

    # Fungsi untuk memuat gambar yang akan diperiksa
    def load_image_to_inspect():
        file_path = filedialog.askopenfilename(title="Pilih Gambar yang Akan Diperiksa", filetypes=[("File Gambar", "*.png *.jpg *.jpeg")])
        if file_path:
            frame = cv2.imread(file_path)
            return frame
        else:
            return None

    # Fungsi untuk memperbarui tampilan dengan hasil inspeksi
    def update_display():
        # Muat gambar untuk inspeksi
        frame = load_image_to_inspect()

        if frame is not None:
            # Lakukan inspeksi kualitas
            result, ssim_value, frame_with_boxes = quality_inspection(frame, reference_image)

        # Display result with SSIM value
        if result == "Good":
          cv2.putText(frame_with_boxes, f"Result: {result}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
          cv2.putText(frame_with_boxes, f"Result: {result}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
          
        cv2.putText(frame_with_boxes, f"SSIM: {ssim_value:.2f}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # Show frame
        cv2.imshow('Quality Inspection', frame_with_boxes)
        cv2.imshow('Reference Image', reference_image)
        
        cv2.destroyAllWindows()

# Tombol untuk memuat gambar untuk inspeksi
load_inspection_button = ttk.Button(root, text="Muat Gambar untuk Inspeksi", command=update_display)
load_inspection_button.pack(pady=10)

# Tombol untuk mengganti gambar referensi
change_reference_button = ttk.Button(root, text="Ganti Gambar Referensi",command=load_reference_image)
change_reference_button.pack(pady=10)

# Jalankan loop Tkinter
root.mainloop()
