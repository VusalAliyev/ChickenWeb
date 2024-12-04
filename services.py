import cv2
import os
from pathlib import Path

class FrameExtractorService:
    def __init__(self, root_path: str = "./frames"):
        self.root_path = root_path
        Path(self.root_path).mkdir(parents=True, exist_ok=True)

    def extract_frames(self, video_path: str, frame_interval: int):
        video_capture = cv2.VideoCapture(video_path)
        if not video_capture.isOpened():
            raise ValueError("Could not open the video file.")

        frame_count = 0
        saved_frame_count = 0
        frames_dir = os.path.join(self.root_path, Path(video_path).stem)
        os.makedirs(frames_dir, exist_ok=True)

        while True:
            ret, frame = video_capture.read()
            if not ret:
                break

            if frame_count % frame_interval == 0:
                frame_path = os.path.join(frames_dir, f"frame_{saved_frame_count}.jpg")
                cv2.imwrite(frame_path, frame)
                saved_frame_count += 1

            frame_count += 1

        video_capture.release()
        return frames_dir
