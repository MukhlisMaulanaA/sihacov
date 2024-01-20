import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

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

        # Resolusi gambar dalam DPI (dots per inch)
        self.image_resolution = (400, 400)  # Gantilah dengan nilai resolusi yang sesuai
        # Ukuran fisik gambar dalam sentimeter
        self.image_size_cm = (2, 5)  # Gantilah dengan ukuran fisik yang sesuai

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Image", command=self.open_image)

        save_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Save", menu=save_menu)
        save_menu.add_command(label="Save Bounding Boxes", command=self.save_bounding_boxes)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            self.image = Image.open(file_path)
            self.display_image()

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
        pixels_per_cm_x = self.image_resolution[0] / 2.54  # Faktor konversi piksel ke cm (resolusi X)
        pixels_per_cm_y = self.image_resolution[1] / 2.54  # Faktor konversi piksel ke cm (resolusi Y)

        width_cm = abs(x2 - x1) / pixels_per_cm_x
        height_cm = abs(y2 - y1) / pixels_per_cm_y

        area_cm2 = width_cm * height_cm
        return area_cm2

    def save_bounding_boxes(self):
        # Implement the code to save bounding box data to your storage system (database, file, etc.)
        print("Bounding Boxes Saved:", self.bounding_boxes)

if __name__ == "__main__":
    root = tk.Tk()
    app = BoundingBoxApp(root)
    root.mainloop()
