import cv2
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk

# Faktor konversi dari piksel ke sentimeter
faktor_konversi = 0.1
area_cm_fix = 160.00
toleransi = 0.0

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

        self.btn_register = ttk.Button(self.root, text="Register", command=self.register_image)
        self.btn_register.pack(pady=10)

        self.label_tolerance = ttk.Label(self.root, text="Toleransi Bounding Box:")
        self.label_tolerance.pack(pady=5)

        self.scale_tolerance = ttk.Scale(self.root, from_=0, to=10, orient=tk.HORIZONTAL, length=200, command=self.update_tolerance)
        self.scale_tolerance.set(toleransi)
        self.scale_tolerance.pack(pady=10)

        self.btn_inspect = ttk.Button(self.root, text="Mulai Inspeksi", command=self.start_inspection)
        self.btn_inspect.pack(pady=10)
        
        # Tambahkan variabel untuk melacak titik awal dan akhir dari bounding box
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None

        # Tambahkan binding mouse event
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)

        # Inisialisasi daftar untuk menyimpan informasi gambar dan bounding box dari register
        self.registered_images = []

        # Inisialisasi variabel untuk melacak mode register
        self.register_mode = False
        self.register_image_path = None
        self.register_bounding_box = None

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

    def register_image(self):
        # Fungsi untuk register gambar
        file_path = filedialog.askopenfilename(title="Pilih Gambar", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])

        if file_path:
            # Simpan path gambar yang di-register
            self.register_image_path = file_path

            # Buka gambar dan tampilkan di GUI
            image = cv2.imread(file_path)
            self.show_image_in_gui(image)

            # Tampilkan pesan untuk menggambar bounding box
            print("Silakan gambar bounding box pada gambar dengan menekan dan menarik mouse.")

            # Set mode register menjadi True
            self.register_mode = True

    def show_image_in_gui(self, image):
        # Fungsi untuk menampilkan gambar di GUI
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image=Image.fromarray(image))
        self.canvas.config(width=photo.width(), height=photo.height())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.root.update_idletasks()  # Update tampilan GUI

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
                
            # Tambahkan logika register
            if self.register_mode:
                # Dapatkan bounding box dari pengguna (contoh: menggunakan mouse event)
                # ...

                # Setelah pengguna selesai menggambar bounding box
                # Simpan bounding box dan kembalikan mode register menjadi False
                self.register_bounding_box = (x, y, w, h)
                self.registered_images.append({
                    'image_path': self.register_image_path,
                    'bounding_box': self.register_bounding_box
                })
                print("Gambar berhasil diregistrasi.")
                self.register_mode = False

            self.root.after(10, self.update)
        else:
            self.cap.release()
            
    def on_mouse_press(self, event):
        # Fungsi untuk menangani event mouse click
        self.start_x = event.x
        self.start_y = event.y

    def on_mouse_drag(self, event):
        # Fungsi untuk menangani event mouse drag (menggambar bounding box)
        self.end_x = event.x
        self.end_y = event.y

        # Gambar bounding box yang sedang ditarik
        self.canvas.delete("bbox")  # Hapus bounding box sebelumnya
        self.canvas.create_rectangle(self.start_x, self.start_y, self.end_x, self.end_y, outline="red", tags="bbox")

    def on_mouse_release(self, event):
        # Fungsi untuk menangani event mouse release
        self.end_x = event.x
        self.end_y = event.y

        # Gambar bounding box yang telah selesai
        self.canvas.delete("bbox")  # Hapus bounding box sebelumnya
        self.canvas.create_rectangle(self.start_x, self.start_y, self.end_x, self.end_y, outline="red", tags="bbox")

        # Simpan bounding box ke dalam daftar registered_images
        self.register_bounding_box = (self.start_x, self.start_y, self.end_x, self.end_y)
        self.registered_images.append({
            'image_path': self.register_image_path,
            'bounding_box': self.register_bounding_box
        })
        print("Gambar berhasil diregistrasi.")
        self.register_mode = False

    def update_tolerance(self, value):
        # Fungsi untuk mengatur nilai toleransi dari GUI
        global toleransi
        toleransi = float(value)

    def start_inspection(self):
        # Fungsi untuk memulai proses inspeksi dengan menggunakan informasi dari register
        for registered_image in self.registered_images:
            image_path = registered_image['image_path']
            bounding_box = registered_image['bounding_box']
            
            # Lakukan proses inspeksi sesuai kebutuhan
            # Tambahkan logika untuk capture frame jika tombol spasi ditekan

            # Tampilkan informasi hasil inspeksi ke GUI (contoh: menampilkan luas bounding box)
            area_px = (bounding_box[2] - bounding_box[0]) * (bounding_box[3] - bounding_box[1])
            area_cm = area_px * faktor_konversi * faktor_konversi

            print(f"Informasi Inspeksi - Gambar: {image_path}, Luas Bounding Box: {area_cm:.2f} cm^2")

if __name__ == "__main__":
    video_source = "./test2.mp4"
    root = tk.Tk()
    app = BoundingBoxApp(root, video_source)
    root.mainloop()
