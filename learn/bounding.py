import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class BoundingBoxApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bounding Box App")

        self.canvas = tk.Canvas(root)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        self.image_path = None
        self.image = None
        self.photo = None
        self.rect_id = None
        self.start_x = None
        self.start_y = None

        self.label = tk.Label(root, text="Luas Bounding Box: -", font=("Helvetica", 12))
        self.label.pack(pady=10)

        self.status_label = tk.Label(root, text="Silakan pilih gambar terlebih dahulu.", font=("Helvetica", 10))
        self.status_label.pack(pady=5)

        open_button = tk.Button(root, text="Pilih Gambar", command=self.open_image)
        open_button.pack(pady=10)

        clear_button = tk.Button(root, text="Hapus Bounding Box", command=self.clear_bbox)
        clear_button.pack(pady=5)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            self.image_path = file_path
            self.load_image()
            self.status_label.config(text=f"Gambar terpilih: {self.image_path}")

    def load_image(self):
        self.image = cv2.imread(self.image_path)
        self.display_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.display_image))

        self.canvas.config(width=self.image.shape[1], height=self.image.shape[0])
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

    def clear_bbox(self):
        if self.rect_id:
            self.canvas.delete(self.rect_id)
            self.rect_id = None
            self.start_x = None
            self.start_y = None
            self.label.config(text="Luas Bounding Box: -")
            self.status_label.config(text="Bounding Box dihapus.")

    def on_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)

    def on_drag(self, event):
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)

        if self.rect_id:
            self.canvas.delete(self.rect_id)

        self.rect_id = self.canvas.create_rectangle(self.start_x, self.start_y, cur_x, cur_y, outline='red')

    def on_release(self, event):
        end_x = self.canvas.canvasx(event.x)
        end_y = self.canvas.canvasy(event.y)

        width_px = abs(end_x - self.start_x)
        height_px = abs(end_y - self.start_y)

        area_px = width_px * height_px

        # Asumsi resolusi 1 piksel = 1 cm (harap sesuaikan dengan resolusi sebenarnya)
        resolusi_x = 14
        resolusi_y = 14

        area_cm2 = area_px / (resolusi_x * resolusi_y)

        self.label.config(text=f"Luas Bounding Box: {area_cm2:.2f} cm²")
        self.status_label.config(text="Bounding Box ditentukan.")


    def run(self):
        self.root.mainloop()

root = tk.Tk()
app = BoundingBoxApp(root)
app.canvas.bind("<ButtonPress-1>", app.on_press)
app.canvas.bind("<B1-Motion>", app.on_drag)
app.canvas.bind("<ButtonRelease-1>", app.on_release)
app.run()
