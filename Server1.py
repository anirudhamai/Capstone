from flask import Flask, render_template, Response
import socket
import cv2
from ultralytics import YOLO
import numpy as np
from sort1 import Sort
from datetime import datetime
from threading import Thread
import threading
import cvzone
import math
from sms_alert import send_sms

app = Flask(__name__)

received_video_filename = None

# to establish socket and store
def receive_video():
    global received_video_filename
    SERVER_HOST = 'localhost'  
    SERVER_PORT = 8502

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))

    server_socket.listen(1)
    print(f"[*] Listening on {SERVER_HOST}:{SERVER_PORT}")

    client_socket, client_address = server_socket.accept()
    print(f"[*] Accepted connection from {client_address}")

    received_video_filename = 'received_video6.mp4'
    with open(received_video_filename, 'wb') as f:
        while True:
            chunk_size_bytes = client_socket.recv(4)
            if not chunk_size_bytes:
                break
            chunk_size = int.from_bytes(chunk_size_bytes, byteorder='big')
            video_data = client_socket.recv(chunk_size)
            if not video_data:
                break
            f.write(video_data)

    print("[*] Video received successfully.")

    cap = cv2.VideoCapture(received_video_filename)
    model = YOLO(r"C:\Users\91827\Desktop\Capstone\yolov9c.pt")

    classNames = ['person', 'bicycle', 'car', 'motorbike', 'aeroplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
              'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant',
              'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard',
              'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle',
              'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli',
              'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'sofa', 'potted plant', 'bed', 'dining table', 'toilet',
              'tv monitor', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink',
              'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']
    
    tracker = Sort(max_age = 25, min_hits = 3, iou_threshold = 0.5)
    tracker_dict = {}         # Dictionary to store tracking information for objects
    blink_text = True          # To make the "Loitering..!" text blink
    frame_count = 0            # Counter for frames to control blinking
    captured_first_frame = {}            # Dictionary to track if the first frame for each object is captured
    is_loitering = False
    # Get video properties
    w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
    output_video = cv2.VideoWriter("object_tracking_servers.avi",
                       cv2.VideoWriter_fourcc(*'mp4v'),
                       fps,
                       (w, h))

    while True :
        # Read a frame from the video capture
        ret, frame = cap.read()

        # Checks whether the frame was read successfully or not
        if not ret :
            break

        frame = cv2.resize(frame, (640, 480))

        # Use the model to detect objects in the current frame and enable streaming display
        results = model(frame, stream = True)
                #stream : function will treat the input as a continuous stream of frames, such as a video

        # Initialize an empty array to store detected object information
        detections = np.empty((0, 5))           #(0 rows & 5 cols) to store the bounding box coordinates and its conf

        # To extract info from the results of obj detection
        for r in results :
            boxes = r.boxes        # Get the bounding boxes of detected objects in this result
            for box in boxes :
                # Extract the coordinates of the bounding box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)     # Convert the coordinates to integers
                # Calculate and round the confidence score / predicted accuracy
                conf = math.ceil((box.conf[0] * 100)) / 100
                # Get the class label index of the detected object
                cls = int(box.cls[0])
                # Name of the detected class using the index
                currentClass = classNames[cls]

                if currentClass == 'person' :
                    # Create an array with object information
                    currentArray = np.array([x1, y1, x2, y2, conf])
                    # To stack vertically (means to append each detections vertically)
                    detections = np.vstack((detections, currentArray))
                    # print("detection")
                    # print(detections)

        # Update tracker with the new bounding box (list of detections)
        resultsTracker = tracker.update(detections)
            #The purpose of this line is to update the object tracker with the latest information about the detected "person" objects.

        # Tracked results


        for res in resultsTracker :
            # print("Res")
            # print(res)
            # Extract the coordinates and ID of the tracked object
            # x1, y1, x2, y2, Id = res
            # x1, y1, x2, y2, Id = int(x1), int(y1), int(x2), int(y2), int(Id)

            x1, y1, x2, y2, *other_values = res
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            Id = int(other_values[4])  # Assuming the ID is at the 5th position in other_values

            # Calculate width and height of the bounding box
            w, h = x2 - x1, y2 - y1

            # If the object ID is not in the tracker dictionary, initialize its data
            if Id not in tracker_dict :
                tracker_dict[Id] = {'bbox' : None, 'Center' : []}

            # Store the bounding box coordinates
            tracker_dict[Id]['bbox'] = [x1, y1, w, h]

            # Calculate center coordinates (center points) of the object
            center_points = x1 + w // 2, y1 + h // 2
            # Append the center coordinates
            tracker_dict[Id]['Center'].append(center_points)

            if Id in tracker_dict :
                # Retrieve the bounding box
                bbox = tracker_dict[Id]['bbox']
            # Draw a corner rectangle around the object's bounding box
            cvzone.cornerRect(frame, bbox, l = 8, rt = 1, colorR = (255, 255, 50))
            # Display the object's ID near the top-left corner of its bounding box
            cv2.putText(frame, f"ID : {Id}", (max(0, bbox[0]), max(0, bbox[1] - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Check if 'traced_path' exists in tracker_dict for the current object (Id)
            if 'traced_path' not in tracker_dict[Id] :
                # If not, initialize 'traced_path' with the current center point
                tracker_dict[Id]['traced_path'] = [center_points]
            else :
                # If already exists, add the current center point to the traced path
                tracker_dict[Id]['traced_path'].append(center_points)

            # Get the traced path of the current object
            tracked_path = tracker_dict[Id]['traced_path']
            # Draw lines between consecutive traced path points to visualize the path
            for i in range(1, len(tracked_path)) :        # It loops through all the center points
                cv2.line(frame, tracked_path[i - 1], tracked_path[i], (0, 255, 255), 1)
                    # Draws a line between the previous center point and the current center point

            if 'variance' not in tracker_dict[Id] :
                # If not, initialize 'variance' with 0
                tracker_dict[Id]['variance'] = 0

            # Check if there are recorded movement center points for the current object
            if len(tracker_dict[Id]['Center']) > 0 :
                # Convert the recorded center points to an array
                points = np.array(tracker_dict[Id]['Center'])

                var_x = np.var(points[:, 0])         # Variance of x-coordinates to measure horizontal movement
                var_y = np.var(points[:, 1])         # Variance of y-coordinates to measure vertical movement
                var = (var_x + var_y) / 2         # Calculate average variance by combining horizontal and vertical variances
                # print("Var")
                # print(var)

                if var > 600 :
                    tracker_dict[Id]['variance'] = var
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.putText(frame, f"Var : {round(tracker_dict[Id]['variance'], 2)}", (x1, y1 - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    # After every 15 frames, it will toggle the "Loitering..!" text
                    if frame_count % 15 == 0 :
                        blink_text = not blink_text
                    frame_count += 1      # Increment the frame count


                    if frame_count % 15 == 0 :
                        blink_text = not blink_text
                        frame_count += 1
                        if flag==0:
                            send_sms("Loitering activity detected!")
                            flag=1
                    # Display a warning text for potential loitering
                    if blink_text :
                        cv2.putText(frame, f'Loitering..!', (30, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

                    # Check if the first frame of loitering is captured for this object ID
                    if not captured_first_frame.get(Id, False) :
                        loitering_start_time = datetime.now()       # Get the current time as the start time of loitering
                        captured_first_frame[Id] = True          # Mark that the first frame has been captured

                        # Get the current time and format
                        timestamp = loitering_start_time.strftime('%d/%m/%Y - %H:%M:%S')
                        loitering_text = f'Loitering Start : {timestamp}'
                        # Display the loitering start text on the frame
                        cvzone.putTextRect(frame, loitering_text, (max(30, 10), max(450, 35)), font = cv2.FONT_HERSHEY_SIMPLEX,
                                        scale = 0.5,  thickness = 1, colorR = (50, 50, 255))

                        # Save the current frame as an image
                        # img_file = f'Loitering_ID {Id}.jpg'
                        # cv2.imwrite(img_file, frame)

                # If variance is below the threshold
                else :
                    # Check if loitering was previously detected
                    if is_loitering :
                        # Get the current time as the end time of loitering
                        loitering_end_time = datetime.now()
                        # Reset the is_loitering
                        is_loitering = False
                        # Calculate the duration of loitering
                        loitering_duration = (loitering_end_time - loitering_start_time).seconds
                        # Display loitering end time text on the frame
                        cvzone.putTextRect(frame, loitering_text, (max(30, 10), max(450, 35)), font = cv2.FONT_HERSHEY_SIMPLEX,
                                        scale = 0.5,  thickness = 1, colorR = (50, 50, 255))

        # Display the Video
        # cv2_imshow(frame)

        # Write frame to video writer
        output_video.write(frame)
        # result.write(frame)
        if cv2.waitKey(1) == ord('q') :
            break

        # Release the video capture and close OpenCV windows
        cap.release()
        cv2.destroyAllWindows()


    client_socket.close()
    server_socket.close()

lock = threading.Lock()
received_video = None

# convert the stored video to frames so as to display in route '/videofeed'
def generate_frame():
    # global received_video

    # cap = cv2.VideoCapture(received_video_filename)
    # if not cap.isOpened():
    #     print("Error: Couldn't open video file.")
    #     return

    # while cap.isOpened():
    #     ret, frame = cap.read()
    #     if not ret:
    #         break
    #     yield (b'--frame\r\n'
    #            b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame)[1].tobytes() + b'\r\n')

    # cap.release()
    # def generate_frame():
    # global received_video
    # while True:
    #     with lock:
    #         if received_video is not None:
    #             # Decode the received video data
    #             frame = cv2.imdecode(np.frombuffer(received_video, dtype=np.uint8), cv2.IMREAD_COLOR)
    #             # Encode the frame as JPEG
    #             ret, jpeg = cv2.imencode('.jpg', frame)
    #             if not ret:
    #                 break
    #             # Yield the encoded frame
    #             yield (b'--frame\r\n'
    #                    b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
    #         else:
    #             break
    cap = cv2.VideoCapture(received_video_filename)
    if not cap.isOpened():
        print("Error: Couldn't open video file.")
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # Encode the frame as JPEG
        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            break
        # Yield the encoded frame
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

    cap.release()


@app.route('/video_feed')
def video_feed():
    print("In video feed")
    return Response(generate_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video')
def index():
    # print(received_video_filename)
    # return '''
    # <!DOCTYPE html>
    # <html lang="en">
    # <head>
    #     <meta charset="UTF-8">
    #     <meta name="viewport" content="width=device-width, initial-scale=1.0">
    #     <title>Video Feed</title>
    # </head>
    # <body>
    #     <h1>Video Feed</h1>
    #     # <video src="/received_video2.mp4" style="width:100%">
    #     <video controls>
    #     <source src="D:\Capstone\received_video2.mp4" type="video/mp4">
    #     Your browser does not support the video tag.
    # </video>
    # </body>
    # </html>
    # '''
    return render_template('index1.html')

receive_thread = Thread(target=receive_video)
receive_thread.start()

if __name__ == '__main__':
    # start_server()
    app.run(host='localhost', port=8504, debug=True)
