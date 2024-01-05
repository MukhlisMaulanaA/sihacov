import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from skimage.metrics import structural_similarity as ssim
import imutils

class QualityControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quality Control App")

        self.cap = cv2.VideoCapture("test2.mp4")
        self.reference_images = [
            ("img\jarum-suntik.jpg", "Good"),
            ("img\jarum-suntik-ng2.jpg", "Not Good")
        ]

        self.label_status = ttk.Label(root, text="Status: Waiting for classification", font=("Helvetica", 12))
        self.label_status.pack(pady=10)

        self.video_label = ttk.Label(root)
        self.video_label.pack()

        self.classify_button = ttk.Button(root, text="Classify", command=self.classify_image)
        self.classify_button.pack(pady=10)

        self.update()
        self.root.mainloop()

    def calculate_image_similarity(self, img1, img2):
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        (score, _) = ssim(gray1, gray2, full=True)
        return score

    def classify_image(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        classified_as = None
        max_similarity = 0

        for ref_image_path, label in self.reference_images:
            ref_image = cv2.imread(ref_image_path)
            similarity = self.calculate_image_similarity(frame, ref_image)

            if similarity > max_similarity:
                max_similarity = similarity
                classified_as = label

        status_text = f"Status: Classified as {classified_as} with similarity {max_similarity:.2f}"
        self.label_status.config(text=status_text)

    def update(self):
        ret, frame = self.cap.read()
        if ret:
            frame = imutils.resize(frame, width=400)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.config(image=imgtk)

        self.root.after(10, self.update)

if __name__ == "__main__":
    root = tk.Tk()
    app = QualityControlApp(root)
