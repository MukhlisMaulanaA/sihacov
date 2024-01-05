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
threshold_value = 0.90
good_objects_count = 0
not_good_objects_count = 0
bounding_box = None

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

def quality_inspection(frame, reference_image):
    global threshold_value, good_objects_count, not_good_objects_count, bounding_box
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_reference = cv2.cvtColor(reference_image, cv2.COLOR_BGR2GRAY)
    ssim_value = ssim(gray_reference, gray_frame)

    if bounding_box is not None:
        x1, y1, x2, y2 = bounding_box
        roi = frame[y1:y2, x1:x2]
        roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        _, thresholded_roi = cv2.threshold(roi_gray, 100, 255, cv2.THRESH_BINARY)
        if cv2.countNonZero(thresholded_roi) == 0:
            return frame
        ssim_roi = ssim(cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY), gray_reference)
        if ssim_roi > threshold_value:
            result = "Good"
            good_objects_count += 1
        else:
            result = "Not Good"
            not_good_objects_count += 1
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(frame, f"ROI: {result}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    return frame

def select_reference_image():
    global reference_image_path

    reference_image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])
    update_reference_image()

def create_bounding_box(event, x, y, flags, param):
    global bounding_box

    if event == cv2.EVENT_LBUTTONDOWN:
        bounding_box = [x, y, x+50, y+50]

def start_inspection():
    global reference_image, cap, inspection_running, good_objects_count, not_good_objects_count
    inspection_running = True
    reference_image = cv2.imread(reference_image_path)
    reference_height, reference_width, _ = reference_image.shape
    cap = cv2.VideoCapture("test1.mp4")
    while inspection_running:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (reference_width, reference_height))
        frame_with_boxes = quality_inspection(frame, reference_image)
        cv2.putText(frame_with_boxes, f"Good: {good_objects_count}", (20, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame_with_boxes, f"Not Good: {not_good_objects_count}", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow("Inspection Process", frame_with_boxes)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    inspection_running = False
    cap.release()
    cv2.destroyAllWindows()

def update_reference_image():
    global reference_image

    # Baca gambar referensi
    reference_image = cv2.imread(reference_image_path)
    cv2.imshow("Reference Image", reference_image)

root_reference = Tk()
root_reference.title("Input Referensi")
frame_reference = Frame(root_reference, width=400, height=400)
frame_reference.pack()
select_button = Button(frame_reference, text="Select Reference Image", command=select_reference_image)
select_button.pack(pady=10)
reference_panel = Label(frame_reference)
reference_panel.pack(padx=10, pady=10)

cv2.namedWindow("Inspection Process")
cv2.setMouseCallback("Inspection Process", create_bounding_box)

root_reference.mainloop()
