import cv2
from skimage.metrics import structural_similarity as ssim

def load_reference_image():
    # Function to load the reference image
    reference_image = cv2.imread('baut-mur.jpg')  # Replace with your reference image
    return reference_image

def quality_inspection(frame, reference_image):
    # Function to perform quality inspection
    
    # Convert both frames to grayscale for SSIM calculation
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_reference = cv2.cvtColor(reference_image, cv2.COLOR_BGR2GRAY)
    
    # Calculate SSIM
    ssim_value = ssim(gray_reference, gray_frame)
    
    # Perform edge detection (using Canny in this example)
    edges_frame = cv2.Canny(gray_frame, 50, 150)
    
    # Find contours in the edge-detected image
    contours, _ = cv2.findContours(edges_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw bounding boxes around detected objects
    frame_with_boxes = frame.copy()  # Create a copy of the frame
    cv2.drawContours(frame_with_boxes, contours, -1, (0, 255, 0), 2)
    
    # Set a threshold for SSIM value
    threshold = 0.95  # Change the threshold value as needed
    
    # Determine the result based on SSIM and threshold
    if ssim_value > threshold:
        result = "Good"
    else:
        result = "Not Good"
    
    return result, ssim_value, frame_with_boxes

# Load reference image
reference_image = load_reference_image()

# Main loop for processing frames
while True:
    # Capture a frame from the camera or load an image
    frame = cv2.imread('lem.jpg')  # Replace with your frame source
    
    # Perform quality inspection
    result, ssim_value, frame_with_boxes = quality_inspection(frame, reference_image)
    
    # Display result with SSIM value
    if result == "Good":
      cv2.putText(frame_with_boxes, f"Result: {result}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    else:
      cv2.putText(frame_with_boxes, f"Result: {result}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
      
    cv2.putText(frame_with_boxes, f"SSIM: {ssim_value:.2f}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # Show frame
    cv2.imshow('Quality Inspection', frame_with_boxes)
    
    # Break loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cv2.destroyAllWindows()
