import cv2
import numpy as np
import csv
from collections import defaultdict
from ultralytics import YOLO
from ultralytics.utils.plotting import colors


#model=yolov5
#result=annotated video
#cap=original video
#results=bounding boxes of detected humans
#track_history= trajectory data



track_history = defaultdict(list)

model = YOLO("yolov5s.pt")
names = model.model.names


video_path = r"C:\Users\91827\Desktop\Capstone\sample_cctv.mkv"
#C:\Users\91827\Desktop\Capstone\sample_cctv.mp4

# Open the video file
cap = cv2.VideoCapture(video_path)
assert cap.isOpened(), "Error reading video file"

# Get video properties
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

result = cv2.VideoWriter("object_tracking.avi",
                       cv2.VideoWriter_fourcc(*'mp4v'),
                       fps,
                       (w, h))

while cap.isOpened():
    success, frame = cap.read()
    if success:
        results = model.track(frame, persist=True, verbose=False)
        boxes = results[0].boxes.xyxy.cpu()

        if results[0].boxes.id is not None:
            clss = results[0].boxes.cls.cpu().tolist()
            track_ids = results[0].boxes.id.int().cpu().tolist()
            confs = results[0].boxes.conf.float().cpu().tolist()

            for box, cls, track_id in zip(boxes, clss, track_ids):
                if names[int(cls)] == 'person':
                    
                    track_history[track_id].append((int((box[0] + box[2]) / 2), int((box[1] + box[3]) / 2)))

                    cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 255, 0), 2)
                    for i in range(1, len(track_history[track_id])):
                        cv2.line(frame, track_history[track_id][i - 1], track_history[track_id][i], (0, 0, 255), 2)

        result.write(frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break


print(track_history)
# traj_data = csv.writer(open("output.csv", "w"))
# for key, val in dict.items():
#     traj_data.writerow([key, val])
result.release()
cap.release()
cv2.destroyAllWindows()