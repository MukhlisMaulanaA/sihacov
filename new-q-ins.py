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
bounding_boxes = []
classifications = []

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

def detect_corners(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    corners = cv2.cornerHarris(gray, 2, 3, 0.04)
    corners = cv2.dilate(corners, None)
    image[corners > 0.01 * corners.max()] = [0, 0, 255]
    return image

def quality_inspection(frame, reference_image):
    global threshold_value, good_objects_count, not_good_objects_count, bounding_boxes, classifications
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_reference = cv2.cvtColor(reference_image, cv2.COLOR_BGR2GRAY)
    ssim_value = ssim(gray_reference, gray_frame)
    edges_frame = cv2.Canny(gray_frame, 50, 150)
    contours, _ = cv2.findContours(edges_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    frame_with_boxes = frame.copy()
    cv2.drawContours(frame_with_boxes, contours, -1, (0, 255, 0), 2)

    for i, bounding_box in enumerate(bounding_boxes):
        if i < len(classifications):
            x1, y1 = bounding_box
            x2, y2 = bounding_box[0] + 50, bounding_box[1] + 50  # Set size of bounding box
            cv2.rectangle(frame_with_boxes, (x1, y1), (x2, y2), (255, 0, 0), 2)
            roi = frame[y1:y2, x1:x2]
            roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            _, thresholded_roi = cv2.threshold(roi_gray, 100, 255, cv2.THRESH_BINARY)
            if cv2.countNonZero(thresholded_roi) == 0:
                continue
            ssim_roi = ssim(cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY), gray_reference)
            if ssim_roi > threshold_value:
                result = "Good"
                good_objects_count += 1
            else:
                result = "Not Good"
                not_good_objects_count += 1
            cv2.putText(frame_with_boxes, f"{classifications[i]}: {result}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    return frame_with_boxes

def select_reference_image():
    global reference_image_path, bounding_boxes

    # Reset bounding boxes
    bounding_boxes = []

    reference_image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])
    update_reference_image()

    # Set mouse callback function
    cv2.namedWindow("Reference Image")
    cv2.setMouseCallback("Reference Image", create_bounding_box)

def create_bounding_box(event, x, y, flags, param):
    global bounding_boxes

    if event == cv2.EVENT_LBUTTONDOWN:
        bounding_boxes.append((x, y))

        if len(bounding_boxes) == 2:
            cv2.rectangle(reference_image, bounding_boxes[0], bounding_boxes[1], (0, 255, 0), 2)
            cv2.imshow("Reference Image", reference_image)

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
        frame_with_boxes = detect_corners(frame_with_boxes)
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

def draw_bounding_box(event, x, y, flags, param):
    global reference_image, bounding_boxes, classifications
    if event == cv2.EVENT_LBUTTONDOWN:
        bounding_boxes.append((x, y))
    elif event == cv2.EVENT_RBUTTONDOWN:
        classification = simpledialog.askstring("Classification", "Enter classification:")
        if classification is not None:
            classifications.append(classification)

root_reference = Tk()
root_reference.title("Input Referensi")
frame_reference = Frame(root_reference, width=400, height=400)
frame_reference.pack()
select_button = Button(frame_reference, text="Select Reference Image", command=select_reference_image)
select_button.pack(pady=10)
reference_panel = Label(frame_reference)
reference_panel.pack(padx=10, pady=10)

root_inspection = Toplevel()
root_inspection.title("Proses Inspeksi")
frame_inspection = Frame(root_inspection, width=400, height=400)
frame_inspection.pack()
start_button = Button(frame_inspection, text="Start Inspection", command=start_inspection_thread)
start_button.pack(pady=10)
stop_button = Button(frame_inspection, text="Stop Inspection", command=stop_inspection)
stop_button.pack(pady=10)
change_threshold_button = Button(frame_inspection, text="Change Threshold", command=change_threshold)
change_threshold_button.pack(pady=10)
panel = Label(frame_inspection)
panel.pack(padx=10, pady=10)

root_reference.mainloop()
root_inspection.mainloop()
