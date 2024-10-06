# uncompyle6 version 3.9.2
# Python bytecode version base 3.8.0 (3413)
# Decompiled from: Python 3.8.10 (tags/v3.8.10:3d8993a, May  3 2021, 11:48:03) [MSC v.1928 64 bit (AMD64)]
# Embedded file name: d:\SportsSight\camera_movement_estimator\camera_movement_estimator.py
# Compiled at: 2024-09-27 19:26:44
# Size of source mod 2**32: 4147 bytes
"""
pickle: Used for serializing and deserializing Python objects. 
It allows you to save and load Python data structures (like lists or dictionaries) from files.

"""
import pickle
import cv2
import numpy as np
import os
import sys

sys.path.append("../")
from utils import measure_distance, measure_xy_distance  # noqa: F401


class CameraMovementEstimator:

    def __init__(self, frame):
        self.minimum_distance = 5
        self.lk_params = dict(winSize=(50, 50),
                              maxLevel=2,
                              criteria=(cv2.TERM_CRITERIA_EPS
                                        | cv2.TERM_CRITERIA_COUNT, 50, 0.03))
        first_frame_grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mask_features = np.zeros_like(first_frame_grayscale)
        mask_features[(None [:None], 0 [:20])] = 1
        mask_features[(None [:None], 900 [:1050])] = 1
        self.features = dict(maxCorners=100,
                             qualityLevel=0.3,
                             minDistance=3,
                             blockSize=7,
                             mask=mask_features)

    def add_adjust_positions_to_tracks(self, tracks,
                                       camera_movement_per_frame):
        for object, object_tracks in tracks.items():
            for frame_num, track in enumerate(object_tracks):
                for track_id, track_info in track.items():
                    position = track_info["position"]
                    camera_movement = camera_movement_per_frame[frame_num]
                    position_adjusted = (position[0] - camera_movement[0],
                                         position[1] - camera_movement[1])
                    tracks[object][frame_num][track_id][
                        "position_adjusted"] = position_adjusted

    # def get_camera_movementParse error at or near `ROT_TWO' instruction at offset 46

    def draw_camera_movement(self, frames, camera_movement_per_frame):
        output_frames = []
        for frame_num, frame in enumerate(frames):
            frame = frame.copy()
            overlay = frame.copy()
            cv2.rectangle(overlay, (0, 0), (200, 100), (255, 255, 255), -1)
            alpha = 0.5
            cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
            x_movement, y_movement = camera_movement_per_frame[frame_num]
            frame = cv2.putText(frame, f"Camera Movement X: {x_movement:.2f}",
                                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 0, 0), 3)
            frame = cv2.putText(frame, f"Camera Movement Y: {y_movement:.2f}",
                                (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 0, 0), 3)
            output_frames.append(frame)
        else:
            return output_frames
