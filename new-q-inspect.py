import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np
import threading
import queue

class InspectionSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Inspeksi")

        # Inisialisasi kamera atau sumber video
        self.cap = cv2.VideoCapture("test1.mp4")  # Ganti dengan sumber video atau kamera yang sesuai

        # Inisialisasi variabel algoritma
        self.algo = None
        self.reference = None

        # Mengantrikan frame dari thread citra
        self.queue = queue.Queue()

        # Thread untuk memproses citra dan menampilkan secara real-time
        self.thread = threading.Thread(target=self.update)
        self.thread.daemon = True
        self.thread.start()

        # GUI untuk menu pengaturan
        self.setup_gui()

    def setup_gui(self):
        # Label untuk algoritma
        ttk.Label(self.root, text="Pilih Algoritma:").pack()

        # Pilihan algoritma
        self.algo_var = tk.StringVar(value="Pilih Algoritma")
        algo_options = ["Pendeteksi Cacat", "Deteksi Tepi"]
        ttk.Combobox(self.root, textvariable=self.algo_var, values=algo_options, state="readonly").pack()

        # Tombol untuk memilih gambar referensi
        ttk.Button(self.root, text="Pilih Gambar Referensi", command=self.open_reference).pack()

    def open_reference(self):
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.bmp")])
        if file_path:
            self.algo = 'Pendeteksi Cacat'
            self.reference = cv2.imread(file_path, 0)

    def update(self):
        while True:
            # Baca frame dari kamera atau sumber video
            _, frame = self.cap.read()

            # Proses frame sesuai dengan algoritma yang dipilih
            if self.algo == 'Pendeteksi Cacat':
                if self.reference is not None:
                    res = cv2.matchTemplate(frame, self.reference, cv2.TM_CCOEFF_NORMED)
                    loc = np.where(res >= 0.8)
                    for pt in zip(*loc[::-1]):
                        cv2.rectangle(frame, pt, (pt[0] + self.reference.shape[1], pt[1] + self.reference.shape[0]), (0, 255, 255), 2)

            elif self.algo == 'Deteksi Tepi':
                frame = cv2.Canny(frame, 100, 200)

            # Kirim frame ke antrian
            self.queue.put(frame)

    def display_frame(self):
        while True:
            # Ambil frame dari antrian
            frame = self.queue.get()

            # Tampilkan frame di GUI
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = Image.fromarray(frame)
            frame = ImageTk.PhotoImage(frame)
            self.label.config(image=frame)
            self.label.image = frame

def main():
    root = tk.Tk()

    app = InspectionSystem(root)

    # Membuat GUI untuk display monitoring
    frame_display = ttk.LabelFrame(root, text="Monitoring Citra")
    frame_display.pack(padx=10, pady=10)
    app.label = ttk.Label(frame_display)
    app.label.pack()

    # Memulai thread display monitoring
    display_thread = threading.Thread(target=app.display_frame)
    display_thread.daemon = True
    display_thread.start()

    root.mainloop()

if __name__ == '__main__':
    main()
