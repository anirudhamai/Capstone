import cv2
import numpy as np
from ultralytics import YOLO
from collections import defaultdict
import socket
import pickle

# Initialize YOLO model
model = YOLO("yolov5s.pt")
names = model.model.names

# Initialize defaultdict to store trajectory data
track_history = defaultdict(lambda: [])

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the host and port for communication
host = "localhost"
port = 5000

# Bind the socket to the host and port
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen(1)

print("Server is listening...")

# Accept incoming connection
client_socket, addr = server_socket.accept()
print(f"Connection established with {addr}")

# Open video file
video_path =  r"C:\Users\91827\Desktop\Capstone\sample_cctv.mkv"
cap = cv2.VideoCapture(video_path)
assert cap.isOpened(), "Error reading video file"

# Get video properties
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

frame_data = {'width': w, 'height': h}
frame_data_bytes = pickle.dumps(frame_data)
client_socket.send(frame_data_bytes)



# Initialize video writer
result = cv2.VideoWriter("object_tracking_server.avi",
                       cv2.VideoWriter_fourcc(*'mp4v'),
                       fps,
                       (w, h))

# Process video frames
while cap.isOpened():
    success, frame = cap.read()
    if success:
        # Perform object tracking using YOLO
        results = model.track(frame, persist=True, verbose=False)
        boxes = results[0].boxes.xyxy.cpu()

        if results[0].boxes.id is not None:
            clss = results[0].boxes.cls.cpu().tolist()
            track_ids = results[0].boxes.id.int().cpu().tolist()
            confs = results[0].boxes.conf.float().cpu().tolist()

            # Iterate through detected objects
            for box, cls, track_id in zip(boxes, clss, track_ids):
                # Filter out only 'person' class
                if names[int(cls)] == 'person':
                    # Store tracking history
                    track_history[track_id].append((int((box[0] + box[2]) / 2), int((box[1] + box[3]) / 2)))

                    # Draw bounding box and trajectory
                    cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 255, 0), 2)
                    for i in range(1, len(track_history[track_id])):
                        cv2.line(frame, track_history[track_id][i - 1], track_history[track_id][i], (0, 0, 255), 2)
                        
                    # Send trajectory data to client
                    data = {'id': track_id, 'trajectory': track_history[track_id]}
                    data_str = pickle.dumps(data)
                    client_socket.sendall(data_str)

        # Write frame to video writer
        result.write(frame)

        # Exit loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break

# Close client socket
client_socket.close()

# Release video capture and video writer objects
result.release()
cap.release()
cv2.destroyAllWindows()
