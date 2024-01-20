import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Faktor konversi dari piksel ke sentimeter
faktor_konversi = 0.1
area_cm_fix = 160.00

class BoundingBoxApp:
    def __init__(self, root, video_source):
        self.root = root
        self.root.title("BoundingBox App")

        self.video_source = video_source
        self.cap = cv2.VideoCapture(self.video_source)

        self.label = ttk.Label(self.root, text="Estimasi Luas")
        self.label.pack(pady=10)

        self.canvas = tk.Canvas(self.root)
        self.canvas.pack()

        self.btn_capture = ttk.Button(self.root, text="Capture", command=self.capture_frame)
        self.btn_capture.pack(pady=10)
        
        

        self.capture_mode = False
        self.counter = 0
        self.frame = None  # Inisialisasi frame sebagai atribut instance

        self.update()

    def capture_frame(self):
        self.capture_mode = not self.capture_mode
        if self.capture_mode:
            print("Capture mode ON")
        else:
            print("Capture mode OFF")

            # Tambahkan logika untuk menyimpan gambar (frame) saat mode capture dimatikan
            if self.capture_mode:
                self.counter += 1
                filename = f'capture_{self.counter}.jpg'
                cv2.imwrite(f"captures-folder/{filename}", self.frame)
                print(f"Frame captured and saved as '{filename}'")

    def update(self):
        ret, frame = self.cap.read()
        if ret:
            self.frame = frame

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

                if not self.capture_mode:
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

            # Tampilkan frame pada GUI
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.config(width=self.photo.width(), height=self.photo.height())
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

            # Tambahkan logika untuk capture frame jika tombol spasi ditekan
            key = cv2.waitKey(1)
            if key == ord('q'):
                self.cap.release()
                self.root.destroy()
            elif key == ord(' '):
                self.capture_frame()

            self.root.after(10, self.update)
        else:
            self.cap.release()

if __name__ == "__main__":
    video_source = "./test2.mp4"
    root = tk.Tk()
    app = BoundingBoxApp(root, video_source)
    root.mainloop()
