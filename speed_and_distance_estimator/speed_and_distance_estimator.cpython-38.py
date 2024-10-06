# uncompyle6 version 3.9.2
# Python bytecode version base 3.8.0 (3413)
# Decompiled from: Python 3.8.10 (tags/v3.8.10:3d8993a, May  3 2021, 11:48:03) [MSC v.1928 64 bit (AMD64)]
# Embedded file name: d:\SportsSight\speed_and_distance_estimator\speed_and_distance_estimator.py
# Compiled at: 2024-09-27 23:17:04
# Size of source mod 2**32: 4018 bytes
import cv2, sys
sys.path.append("../")
from utils import measure_distance, get_foot_position

class SpeedAndDistance_Estimator:

    def __init__(self):
        self.frame_window = 5
        self.frame_rate = 24

    def add_speed_and_distance_to_tracks(self, tracks):
        total_distance = {}
        for object, object_tracks in tracks.items():
            if not object == "ball":
                if object == "referees":
                    pass
                else:
                    number_of_frames = len(object_tracks)
                    for frame_num in range(0, number_of_frames, self.frame_window):
                        last_frame = min(frame_num + self.frame_window, number_of_frames - 1)

        for track_id, _ in object_tracks[frame_num].items():
            if track_id not in object_tracks[last_frame]:
                pass
            else:
                start_position = object_tracks[frame_num][track_id]["position_transformed"]
                end_position = object_tracks[last_frame][track_id]["position_transformed"]
                if not start_position is None:
                    if end_position is None:
                        pass
                    else:
                        distance_covered = measure_distance(start_position, end_position)
                        time_elapsed = (last_frame - frame_num) / self.frame_rate
                        speed_meters_per_second = distance_covered / time_elapsed
                        speed_km_per_hour = speed_meters_per_second * 3.6
                        if object not in total_distance:
                            total_distance[object] = {}
                        if track_id not in total_distance[object]:
                            total_distance[object][track_id] = 0
                        total_distance[object][track_id] += distance_covered
                        for frame_num_batch in range(frame_num, last_frame):
                            if track_id not in tracks[object][frame_num_batch]:
                                pass
                            else:
                                tracks[object][frame_num_batch][track_id]["speed"] = speed_km_per_hour
                                tracks[object][frame_num_batch][track_id]["distance"] = total_distance[object][track_id]

    def draw_speed_and_distance(self, frames, tracks):
        output_frames = []
        for frame_num, frame in enumerate(frames):
            frame = frame.copy()
            for object, object_tracks in tracks.items():
                if not object == "ball":
                    if object == "referees":
                        pass
                    else:
                        for _, track_info in object_tracks[frame_num].items():
                            if "speed" in track_info:
                                speed = track_info.get("speed", None)
                                distance = track_info.get("distance", None)
                                if not speed is None:
                                    if distance is None:
                                        pass
                                    else:
                                        bbox = track_info["bbox"]
                                        position = get_foot_position(bbox)
                                        position = list(position)
                                        position[1] += 40
                                        position = tuple(map(int, position))
                                        cv2.putText(frame, f"{speed:.2f} km/h", position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,
                                                                                                                          0,
                                                                                                                          0), 2)
                                        cv2.putText(frame, f"{distance:.2f} m", (position[0], position[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,
                                                                                                                                                 0,
                                                                                                                                                 0), 2)
                        else:
                            output_frames.append(frame)

                return output_frames
