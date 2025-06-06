import cv2
import mediapipe as mp
import json
import os
import sys
import numpy as np

def is_valid_landmarks(landmarks):
    for lm in landmarks:
        if not (0 <= lm.x <= 1 and 0 <= lm.y <= 1):
            return False
    return True

def visibility_score(landmarks):
    return sum(lm.visibility for lm in landmarks) / len(landmarks)

def interpolate_landmarks(landmarks1, landmarks2, alpha):
    interpolated = []
    for lm1, lm2 in zip(landmarks1, landmarks2):
        interpolated.append({
            "x": lm1["x"] * (1 - alpha) + lm2["x"] * alpha,
            "y": lm1["y"] * (1 - alpha) + lm2["y"] * alpha,
            "z": lm1["z"] * (1 - alpha) + lm2["z"] * alpha,
            "visibility": lm1["visibility"] * (1 - alpha) + lm2["visibility"] * alpha
        })
    return interpolated

def fill_missing_frames(frames):
    for i in range(1, len(frames) - 1):
        if frames[i] is None and frames[i-1] and frames[i+1]:
            frames[i] = interpolate_landmarks(frames[i-1], frames[i+1], 0.5)
    return frames

def extract_pose_data(video_path, output_json):
    print(f"Starting pose extraction from: {video_path}")
    
    try:
        mp_pose = mp.solutions.pose
        mp_drawing = mp.solutions.drawing_utils
        pose = mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise IOError(f"Could not open video: {video_path}")
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        print(f"Video info: {width}x{height} at {fps:.2f} FPS, {frame_count} frames")
        
        pose_data = {
            "fps": fps,
            "frameCount": frame_count,
            "width": width,
            "height": height,
            "frames": []
        }

        frame_index = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if frame_index % (frame_count // 10) == 0:
                print(f"Processing frame {frame_index}/{frame_count} ({frame_index/frame_count:.0%})")

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(frame_rgb)

            frame_landmarks = []
            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                avg_vis = visibility_score(landmarks)

                if avg_vis > 0.4:
                    frame_landmarks = [{
                        "x": lm.x,
                        "y": lm.y,
                        "z": lm.z,
                        "visibility": lm.visibility
                    } for lm in landmarks]
                else:
                    frame_landmarks = None
            else:
                frame_landmarks = None

            if frame_landmarks is None:
                if len(pose_data["frames"]) > 0:
            
                    pose_data["frames"].append(pose_data["frames"][-1])
                else:
            
                    pose_data["frames"].append([])
            else:
                pose_data["frames"].append(frame_landmarks)

            frame_index += 1
        cap.release()
        cv2.destroyAllWindows()

        if not any(pose_data["frames"]):
            raise ValueError("No valid pose data found in video")


        pose_data["frames"] = fill_missing_frames(pose_data["frames"])

        with open(output_json, 'w') as f:
            json.dump(pose_data, f, indent=2)
        
        print(f"\nSuccess! Pose data saved to {output_json}")
        print(f"Extracted {len([f for f in pose_data['frames'] if f])} valid frames of pose data")
        return True

    except Exception as e:
        print(f"\nError: {str(e)}", file=sys.stderr)
        return False

if __name__ == "__main__":
    input_video = "dance_reference.mp4"
    output_file = "dance_data.json"

    print("Pose Data Extractor")
    print("------------------")

    success = extract_pose_data(input_video, output_file)

    if not success:
        print("\nTroubleshooting tips:")
        print("1. Verify the input video path is correct")
        print("2. Ensure the video contains visible human poses")
        print("3. Check you have write permissions for the output directory")
        print("4. Try with a shorter video clip first")
        sys.exit(1)
