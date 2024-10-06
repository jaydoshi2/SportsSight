from ultralytics import YOLO
import supervision as sv
import pickle
import os
import numpy as np
# import pandas as pd
import cv2
import sys
sys.path.append('../')
from utils import get_center_of_bbox, get_bbox_width, get_foot_position  # noqa: F401


class Tracker:

    def __init__(self, model_path):
        self.model = YOLO(model_path)
        self.tracker = sv.ByteTrack()

    def detect_frames(self, frames):
        batch_size = 20
        detectiions = []
        """
        detectiions will have 
            [
                { 
                    "bbox": [x1, y1, x2, y2],  # Bounding box coordinates
                    "class": "player",         # Class label (e.g., "player", "goalkeeper", "ball")
                    "confidence": 0.92         # Confidence score
                },
                {
                    "bbox": [x1, y1, x2, y2],
                    "class": "ball",
                    "confidence": 0.85
                }
            ]        
            Bounding Boxes: Coordinates that define the area in the frame where the object was detected.
            Class Labels: Each detected object is classified as a specific class (e.g., player, goalkeeper, ball, etc.), based on the YOLO models training.
            Confidence Scores: A value between 0 and 1 representing the confidence level of the detection (must be at least 0.1 due to the threshold set).
            Other Data: Depending on the version of YOLO, additional data may be included, such as object IDs, names , frameNo etc.
        """

        for i in range(0, len(frames), batch_size):
            batch = self.model.predict(frames[i:i + batch_size], conf=0.1)
            detectiions += batch

        return detectiions

    def get_object_tracks(self, frames, read_from_stub=False, stub_path=None):
        
        

        if read_from_stub and stub_path is not None and os.path.exists(
                stub_path):
            with open(stub_path, 'rb') as f:
                tracks = pickle.load(f)
            return tracks

        detections = self.detect_frames(frames)
        print('DETECTIONS ', detections)
        tracks = {"players": [], "referees": [], "ball": []}

        #we are overwriting the goalkeeper with the player
        for frame_num, detection in enumerate(detections):
            cls_names = detection.names
            cls_names_inv = {v: k for k, v in cls_names.items()}
            # info
            """
            frame_num is the index of the current frame, and detection contains the detection results for that frame.
            cls_names: A dictionary containing class IDs mapped to class names (e.g., 0: 'player', 1: 'goalkeeper', 2: 'referee', etc.).
            cls_names_inv: An inverted dictionary that maps class names back to their IDs (e.g., 'player': 0, 'goalkeeper': 1, etc.
            
            """

            # Covert to supervision Detection format
            #Converts the detection results into a format compatible with the supervision library. This format is used for further processing
            detection_supervision = sv.Detections.from_ultralytics(detection)

            # Convert GoalKeeper to player object
            """
            Purpose: Loop through detected objects to change any detected "goalkeeper" to "player".
            This is useful if your tracking logic treats goalkeepers as players for your specific use case.
            Example: If the detection contains a goalkeeper with class_id 1:
            Before: detection_supervision.class_id = [1, 0] (goalkeeper, player)
            After: detection_supervision.class_id = [0, 0] (both as player)
            """
            for object_ind, class_id in enumerate(
                    detection_supervision.class_id):
                if cls_names[class_id] == "goalkeeper":
                    detection_supervision.class_id[object_ind] = cls_names_inv[
                        "player"]

            # Track Objects
            # Passes the detection_supervision to the tracker to associate detections with existing tracks.
            # The tracker will return updated detections that now include tracking information (e.g., track IDs).
            detection_with_tracks = self.tracker.update_with_detections(
                detection_supervision)

            # Initializes empty dictionaries for players, referees, and ball detections for the current frame,
            # to store the bounding boxes and track IDs
            tracks["players"].append({})
            tracks["referees"].append({})
            tracks["ball"].append({})
            """
             Purpose: Loop through the detections returned by the tracker (detection_with_tracks).
            For each detected object:
                bbox: The bounding box of the detected object (coordinates).
                cls_id: The class ID of the detected object.
                track_id: The unique ID assigned by the tracker to identify the object across frames.
                Depending on the class ID, it stores the bounding box in the corresponding tracks dictionary under the frame number and track ID
                
                
                tracks = {
                            "players": [
                                {0: {"bbox": [x1, y1, x2, y2]},  # Track ID 0 for player
                                1: {"bbox": [x3, y3, x4, y4]}}, # Track ID 1 for player
                                ...  # More frames
                            ],
                            "referees": [
                                {2: {"bbox": [x5, y5, x6, y6]}},  # Track ID 2 for referee
                                ...  # More frames
                            ],
                            "ball": [
                                {1: {"bbox": [x7, y7, x8, y8]}},   # Track ID 1 for ball
                                ...  # More frames
                            ]
                        }
            """

            for frame_detection in detection_with_tracks:
                bbox = frame_detection[0].tolist()
                cls_id = frame_detection[3]
                track_id = frame_detection[4]

                if cls_id == cls_names_inv['player']:
                    tracks["players"][frame_num][track_id] = {"bbox": bbox}

                if cls_id == cls_names_inv['referee']:
                    tracks["referees"][frame_num][track_id] = {"bbox": bbox}
            """
            This loop processes detection_supervision directly to check for the ball.
            If the detected object is a ball, it stores the bounding box in the tracks["ball"] dictionary, using a fixed track ID (in this case, 1).
            
            tracks = {
                    "players": [
                        {0: {"bbox": [100, 150, 200, 250]},  # Frame 0, Player 0
                        1: {"bbox": [300, 350, 400, 450]}}, # Frame 0, Player 1
                        {2: {"bbox": [110, 160, 210, 260]}}, # Frame 1, Player 0
                        ...  # Additional frames
                    ],
                    "referees": [
                        {0: {"bbox": [50, 70, 80, 90]}},      # Frame 0, Referee 0
                        {1: {"bbox": [55, 75, 85, 95]}},      # Frame 1, Referee 0
                        ...  # Additional frames
                    ],
                    "ball": [
                        {1: {"bbox": [120, 130, 140, 150]}},  # Frame 0, Ball 0
                        {1: {"bbox": [125, 135, 145, 155]}},  # Frame 1, Ball 0
                        ...  # Additional frames
                    ]
                }
            """
            for frame_detection in detection_supervision:
                bbox = frame_detection[0].tolist()
                cls_id = frame_detection[3]

                if cls_id == cls_names_inv['ball']:
                    tracks["ball"][frame_num][1] = {"bbox": bbox}

            # print("DETECTION SUPERVISION ", detection_supervision)

        # print("TRACKS ", tracks)

        if stub_path is not None:
            with open(stub_path, 'wb') as f:
                pickle.dump(tracks, f)

        return tracks
    def draw_annotations(self,video_frames, tracks):
        output_video_frames= []
        for frame_num, frame in enumerate(video_frames):
            frame = frame.copy() # this is because not to pollute actual video_frames that's why copied the frames

            player_dict = tracks["players"][frame_num]
            ball_dict = tracks["ball"][frame_num]
            referee_dict = tracks["referees"][frame_num]

            # Draw Players
            for track_id, player in player_dict.items():
                color = player.get("team_color",(0,0,255))
                frame = self.draw_ellipse(frame, player["bbox"],color, track_id)

                if player.get('has_ball',False):
                    frame = self.draw_traingle(frame, player["bbox"],(0,0,255))

            # Draw Referee
            for _, referee in referee_dict.items():
                frame = self.draw_ellipse(frame, referee["bbox"],(0,255,255))
            
            # Draw ball 
            for track_id, ball in ball_dict.items():
                frame = self.draw_traingle(frame, ball["bbox"],(0,255,0))


            # Draw Team Ball Control
            # frame = self.draw_team_ball_control(frame, frame_num, team_ball_control)

            
            output_video_frames.append(frame)

        return output_video_frames
    
    
    def draw_ellipse(self,frame,bbox,color,track_id=None):
        y2 = int(bbox[3])
        x_center, _ = get_center_of_bbox(bbox)
        width = get_bbox_width(bbox)

        cv2.ellipse(
            frame,
            center=(x_center,y2),
            axes=(int(width), int(0.35*width)),
            angle=0.0,
            startAngle=-45,
            endAngle=235,
            color = color,
            thickness=2,
            lineType=cv2.LINE_4
        )

        rectangle_width = 20
        rectangle_height=10
        x1_rect = x_center - rectangle_width//2
        x2_rect = x_center + rectangle_width//2
        y1_rect = (y2- rectangle_height//2) +5
        y2_rect = (y2+ rectangle_height//2) +5

        if track_id is not None:
            cv2.rectangle(frame,
                          (int(x1_rect),int(y1_rect) ),
                          (int(x2_rect),int(y2_rect)),
                          color,
                          cv2.FILLED)
            
            x1_text = x1_rect+5 # extra padding of 5 pixels
            if track_id > 99:
                x1_text -=5 #bigger number so reduced the right padding pixels 
            
            cv2.putText(
                frame,
                f"{track_id}",
                (int(x1_text),int(y1_rect+5)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.3,
                (0,0,0),
                1
            )

        return frame
    
    def draw_traingle(self,frame,bbox,color):
        y= int(bbox[1]) # accessing bounding box of ball 
        x,_ = get_center_of_bbox(bbox) # inbuild function to find center of bounding box 

        triangle_points = np.array([
            [x,y], # bottom point coordinate
            [x-5,y-10], # top left point coordinate
            [x+5,y-10], # top right point coordinate
        ])
        cv2.drawContours(frame, [triangle_points],0,color, cv2.FILLED)
        cv2.drawContours(frame, [triangle_points],0,(0,0,0), 2)

        return frame
