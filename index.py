import cv2
import numpy as np

# Load model YOLO
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")

# Load label objek
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Inisialisasi webcam
cap = cv2.VideoCapture(0)

while True:
    # Baca frame dari webcam
    ret, frame = cap.read()
    
    if not ret:
        break
    
    # Membuat blob dari frame
    blob = cv2.dnn.blobFromImage(frame, 1/255, (416, 416), swapRB=True, crop=False)

    # Set input ke model YOLO
    net.setInput(blob)

    # Melakukan deteksi objek
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    outputs = net.forward(output_layers)

    # Menampilkan hasil deteksi
    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:  # Set threshold kepercayaan
                center_x = int(detection[0] * frame.shape[1])
                center_y = int(detection[1] * frame.shape[0])
                width = int(detection[2] * frame.shape[1])
                height = int(detection[3] * frame.shape[0])
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)

                # Gambar bounding box dan label
                cv2.rectangle(frame, (left, top), (left + width, top + height), (0, 255, 0), 2)
                cv2.putText(frame, classes[class_id], (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Menampilkan frame dengan hasil deteksi
    cv2.imshow("Deteksi Objek", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Bebaskan sumber daya
cap.release()
cv2.destroyAllWindows()
