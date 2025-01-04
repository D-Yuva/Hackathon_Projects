from ultralytics import YOLO
import cv2
import cvzone
import math
from deep_sort_realtime.deepsort_tracker import DeepSort

class ObjectDetection():
    def __init__(self, capture=0):
        self.capture = capture
        self.model = self.load_model()
        self.CLASS_NAMES_DICT = self.model.model.names

    def load_model(self):
        model = YOLO('../yolo_weights/yolov8n.pt')
        model.fuse()
        return model

    def predict(self, img):
        results = self.model(img, stream=True)
        return results

    def plot_boxes(self, results, img):
        detections = []
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w, h = x2 - x1, y2 - y1
                cls = int(box.cls[0])
                currentClass = self.CLASS_NAMES_DICT[cls]
                conf = math.ceil(box.conf[0] * 100) / 100
                if conf > 0.5:
                    detections.append((([x1, y1, w, h]), conf, currentClass))
        return detections, img

    def track_detect(self, detections, img, tracker):
        tracks = tracker.update_tracks(detections, frame=img)
        for track in tracks:
            if not track.is_confirmed():
                continue
            track_id = track.track_id
            ltrb = track.to_ltrb()
            bbox = ltrb
            x1, y1, x2, y2 = bbox
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            for det in detections:
                bbox_det, conf, currentClass = det
                x1_det, y1_det, w, h = bbox_det
                if abs(x1 - x1_det) < 10 and abs(y1 - y1_det) < 10:
                    cvzone.putTextRect(img, f'ID: {track_id}', (x1, y1), scale=1, thickness=1, colorR=(0, 0, 255))
                    cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=1, colorR=(255, 0, 255))
                    break
        return img

    def call_(self):
        cap = cv2.VideoCapture(self.capture)
        assert cap.isOpened()

        tracker = DeepSort(
            max_age=5,
            n_init=2,
            nms_max_overlap=1.0,
            max_cosine_distance=0.3,
            nn_budget=None,
            override_track_class=None,
            embedder="mobilenet",
            half=True,
            bgr=True,
            embedder_gpu=True,
            embedder_model_name=None,
            embedder_wts=None,
            polygon=False,
            today=None
        )

        while True:
            ret, img = cap.read()
            assert ret

            results = self.predict(img)
            detections, frames = self.plot_boxes(results, img)
            detect_frame = self.track_detect(detections, frames, tracker)

            cv2.imshow('Image', detect_frame)

            if cv2.waitKey(1) == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

detector = ObjectDetection(capture=0)
detector.call_()
