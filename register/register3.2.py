import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import os

class BoundingBoxApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bounding Box App")

        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        self.bounding_boxes = []
        self.current_bb_start = None

        self.image = None
        self.pixels_per_cm = 0.0264583333  # Faktor konversi piksel ke sentimeter (default: 1 piksel = 0.1 sentimeter)

        self.video_capture = cv2.VideoCapture(0)  # Menggunakan webcam dengan indeks 0 (jika hanya satu webcam)
        
        self.area_values = []  # List untuk menyimpan nilai luas

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Image", command=self.open_image)
        
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Save", menu=file_menu)
        file_menu.add_command(label="Save Bounding Boxes (User)", command=self.save_bounding_boxes)
        
        self.paused = False
        self.pause_button = tk.Button(self.root, text="Pause/Resume", command=self.toggle_pause)
        self.pause_button.pack()
        
        self.update()
    
    def toggle_visualization(self):
        self.visualitation_mode = not self.visualitation_mode
      
    def toggle_pause(self):
        self.paused = not self.paused

    def update(self):
        # Inisialisasi webcam
        if not hasattr(self, 'video_capture'):
            self.video_capture = cv2.VideoCapture(0)

        if not self.paused:
            # Ambil frame dari webcam hanya jika tidak di-pause
            _, frame = self.video_capture.read()

            if frame is not None:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.image = Image.fromarray(frame_rgb)
                self.display_image()

        # Perbarui secara terus-menerus
        self.root.after(10, self.update)
    
    def open_image(self):
        # Ambil frame dari webcam dan simpan sebagai gambar
        _, frame = self.video_capture.read()

        if frame is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Image files", "*.png")])
            if file_path:
                cv2.imwrite(file_path, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    def display_image(self):
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.config(width=self.tk_image.width(), height=self.tk_image.height())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def on_press(self, event):
        x, y = event.x, event.y
        self.current_bb_start = (x, y)

    def on_drag(self, event):
        x, y = event.x, event.y
        if self.current_bb_start:
            self.canvas.delete("temp_bb")  # Hapus bounding box sebelumnya (jika ada)
            self.canvas.create_rectangle(
                self.current_bb_start[0],
                self.current_bb_start[1],
                x, y,
                outline="red", tags="temp_bb"
            )

    def on_release(self, event):
        if self.current_bb_start:
            x1, y1 = self.current_bb_start
            x2, y2 = event.x, event.y
            bounding_box = self.canvas.create_rectangle(
                x1, y1, x2, y2,
                outline="red"
            )
            self.bounding_boxes.append((x1, y1, x2, y2))
            self.current_bb_start = None

            # Hitung dan tampilkan luas bounding box dalam satuan sentimeter persegi
            bounding_box_area_cm2 = self.calculate_area_cm2(x1, y1, x2, y2)
            print("Luas Bounding Box: {:.2f} cm^2".format(bounding_box_area_cm2))

    def calculate_area_cm2(self, x1, y1, x2, y2):
        # Hitung luas bounding box dalam satuan sentimeter persegi
        width_cm = abs(x2 - x1) * self.pixels_per_cm
        height_cm = abs(y2 - y1) * self.pixels_per_cm

        area_cm2 = width_cm * height_cm
        return area_cm2

    def save_bounding_boxes(self):
        # Meminta pengguna untuk memilih lokasi penyimpanan (image)
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])

        if file_path:
            try:
                # Ambil frame dari webcam
                _, frame = self.video_capture.read()

                # Gambar bounding box pada frame
                for bounding_box in self.bounding_boxes:
                    x1, y1, x2, y2 = bounding_box
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # Simpan gambar beserta bounding box
                cv2.imwrite(file_path, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
                print("Image with bounding boxes saved to:", file_path)
            except Exception as e:
                print("Error saving image with bounding boxes:", str(e))

        # Meminta pengguna untuk memilih lokasi penyimpanan (nilai luas)
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

        if file_path:
            try:
                with open(file_path, "w") as file:
                    for bounding_box in self.bounding_boxes:
                        area_cm2 = self.calculate_area_cm2(*bounding_box)
                        bounding_box_str = f"Area: {area_cm2:.2f} cm^2"
                        file.write(bounding_box_str + "\n")
                        
                print("Bounding boxes saved to:", file_path)
            except Exception as e:
                print("Error saving bounding boxes:", str(e))

    def save_area_value(self, area_value):
        # Simpan nilai luas ke dalam list
        self.area_values.append(area_value)
        
if __name__ == "__main__":
    root = tk.Tk()
    app = BoundingBoxApp(root)
    root.mainloop()
