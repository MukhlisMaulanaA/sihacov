import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np

# Global variable to store the reference image
reference_image = None

# Function to handle the 'Register' button click event


def register_image():
    global reference_image
    file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
    if file_path:
        reference_image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        print(f"Reference image registered: {file_path}")

# Function to perform real-time inspection


def inspect_real_time():
    if reference_image is None:
        print("Please register a reference image first.")
        return

    # Use the default camera (you can change the argument to use a different camera)
    cap = cv2.VideoCapture("test2.mp4")

    while True:
        ret, frame = cap.read()

        if ret:
            # Convert the frame to grayscale for processing
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Find contours in the frame
            contours, _ = cv2.findContours(gray_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                # Calculate the area of the contour
                area = cv2.contourArea(contour)

                # Check if the area is within a certain range (you can adjust this threshold)
                min_area = 100
                max_area = 1000
                if min_area < area < max_area:
                    # Draw a bounding box around the object
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    # Compare size with the reference image
                    reference_height, reference_width = reference_image.shape
                    if abs(w - reference_width) < 20 and abs(h - reference_height) < 20:
                        cv2.putText(frame, "Good", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    else:
                        cv2.putText(frame, "Not Good", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                    # Display size and coordinates in the bounding box
                    description = f"Size: {w}x{h}, Coordinates: ({x}, {y})"
                    cv2.putText(frame, description, (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            # Display the result in a separate window
            cv2.imshow("Real-Time Inspection", frame)

            # Exit loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    # Release the camera and destroy all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()


# Initialize the main window
root = tk.Tk()
root.title("Quality Inspection Program")

# Create a 'Register' button
register_button = tk.Button(
    root, text="Register Reference Image", command=register_image)
register_button.pack(pady=20)

# Create a 'Start Inspection' button
inspect_button = tk.Button(
    root, text="Start Inspection", command=inspect_real_time)
inspect_button.pack(pady=10)

# Start the main event loop
root.mainloop()
