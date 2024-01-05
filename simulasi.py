import cv2
from skimage.metrics import structural_similarity as ssim
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog

#== Fungsi untuk memuat gambar referensi ==#
def load_reference_image():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(title="Select Reference Image", filetypes=[("Image Files", "*.png *.jpg *.jpeg")])

    if file_path:
        reference_image = cv2.imread(file_path)
        return reference_image
    else:
        return None

#== Fungsi untuk memuat gambar yang akan diinspeksi ==#
def load_inspection_image():
    root = tk.Tk()
    root.withdraw()  

    file_path = filedialog.askopenfilename(title="Select Image for Inspection", filetypes=[("Image Files", "*.png *.jpg *.jpeg")])

    if file_path:
        inspection_image = cv2.imread(file_path)
        return inspection_image
    else:
        return None

#== Fungsi untuk melakukan Quality Inspection ==#
def quality_inspection(frame, reference_image):
    
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_reference = cv2.cvtColor(reference_image, cv2.COLOR_BGR2GRAY)
    
    ssim_value = ssim(gray_reference, gray_frame)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    blurred = cv2.GaussianBlur(gray_frame, (5, 5), 0)
    
    edges_frame = cv2.Canny(blurred, 50, 100)
    
    dilate = cv2.dilate(edges_frame, kernel, iterations=1)
    
    contours, _ = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    frame_with_boxes = frame.copy() 
    cv2.drawContours(frame_with_boxes, contours, -1, (0, 255, 0), 2)
        
    #== Mengatur nilai Threshold ==#
    threshold = 0.98  
    
    
    #== Proses Klasifikasi Objek menggunakan logika if else ==#
    if ssim_value > threshold:
        result = "Good"
    else:
        result = "Not Good"
    
    return result, ssim_value, frame_with_boxes

#== Membuat variabel gambar referensi dari fungsinya ==#
reference_image = load_reference_image()

#== Jika ada gambar referensinya maka lanjutkan ==#
if reference_image is not None:
    root = tk.Tk()

    #== Fungsi untuk memuat gambar yang akan diinspeksi ==#
    def load_image_to_inspect():
        file_path = filedialog.askopenfilename(title="Pilih Gambar yang Akan Diperiksa", filetypes=[("File Gambar", "*.png *.jpg *.jpeg")])
        if file_path:
            frame = cv2.imread(file_path)
            return frame
        else:
            return None

    #== Fungsi untuk menampilkan proses inspeksi pada GUI ==#
    def update_display():
        frame = load_image_to_inspect()

        if frame is not None:
            result, ssim_value, frame_with_boxes = quality_inspection(frame, reference_image)

        #== Menampilkan keterangan nilai SSIM dan pengklasifikasian ==#
        if result == "Good":
          cv2.putText(frame_with_boxes, f"Result: {result}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
          cv2.putText(frame_with_boxes, f"Result: {result}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
          
        cv2.putText(frame_with_boxes, f"SSIM: {ssim_value:.2f}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        #== Membuka dua buah frame untuk gambar referensi dan inspeksi ==#
        cv2.imshow('Quality Inspection', frame_with_boxes)
        cv2.imshow('Reference Image', reference_image)
        
        cv2.waitKey(0)
        cv2.destroyAllWindows()

#== Membuat Tombol memulai inspeksi ==#
load_inspection_button = ttk.Button(root, text="Muat Gambar untuk Inspeksi", command=update_display)
load_inspection_button.pack(pady=10)

#== Membuat tombol mengganti gambar referensi ==#
change_reference_button = ttk.Button(root, text="Ganti Gambar Referensi",command=load_reference_image)
change_reference_button.pack(pady=10)

#== Memulai GUI Tkinter ==#
root.mainloop()
