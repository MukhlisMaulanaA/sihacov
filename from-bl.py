import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

class App:
    def __init__(self, window):
        self.window = window
        self.window.title("Quality Inspection")

        # Create menu
        self.menu = Menu(self.window)
        self.window.config(menu=self.menu)

        # Create File menu
        self.file_menu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.open_image)
        self.file_menu.add_command(label="Exit", command=self.window.destroy)

        # Create Tools menu
        self.tools_menu = Menu(self.menu)
        self.menu.add_cascade(label="Tools", menu=self.tools_menu)
        self.tools_menu.add_command(label="Register", command=self.register)

        # Create canvas for image display
        self.canvas = Canvas(self.window, width=800, height=600)
        self.canvas.grid(row=0, column=0, padx=10, pady=10)

        # Create label for status message
        self.status_label = Label(self.window, text="Ready", bd=1, relief=SUNKEN, anchor=W)
        self.status_label.grid(row=1, column=0, sticky=W+E)

        # Create frame for ROI
        self.roi_frame = Frame(self.window, bd=2, relief=SUNKEN)
        self.roi_frame.grid(row=0, column=1, padx=10, pady=10, sticky=N+S+W+E)

        # Create label for ROI
        self.roi_label = Label(self.roi_frame, text="Region of Interest")
        self.roi_label.pack(side=TOP, pady=5)

        # Create button for ROI
        self.roi_button = Button(self.roi_frame, text="Define ROI", command=self.define_roi)
        self.roi_button.pack(side=TOP)

        # Create label for ROI coordinates
        self.roi_coords_label = Label(self.roi_frame, text="")
        self.roi_coords_label.pack(side=TOP)

        # Create label for inspection result
        self.inspection_result_label = Label(self.window, text="")
        self.inspection_result_label.grid(row=2, column=0, sticky=W+E)

    def open_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = cv2.imread(file_path)
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.image))
            self.canvas.create_image(0, 0, image=self.photo, anchor=NW)

    def register(self):
        # Add code to register image and parameters
        pass

    def define_roi(self):
        # Add code to define ROI
        pass

    def inspect(self):
        # Add code to perform inspection
        pass

    def update_status(self, message):
        self.status_label.config(text=message)

    def update_inspection_result(self, result):
        self.inspection_result_label.config(text=result)

    def update_roi_coords(self, coords):
        self.roi_coords_label.config(text=f"ROI Coordinates: {coords}")

if __name__ == "__main__":
    window = Tk()
    app = App(window)
    window.mainloop()