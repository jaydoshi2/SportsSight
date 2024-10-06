# uncompyle6 version 3.9.2
# Python bytecode version base 3.8.0 (3413)
# Decompiled from: Python 3.8.10 (tags/v3.8.10:3d8993a, May  3 2021, 11:48:03) [MSC v.1928 64 bit (AMD64)]
# Embedded file name: d:\SportsSight\view_transformer\view_transformer.py
# Compiled at: 2024-09-27 21:10:18
# Size of source mod 2**32: 1878 bytes
import numpy as np, cv2


class ViewTransformer:

    def __init__(self):
        court_width = 68
        court_length = 23.32
        self.pixel_vertices = np.array([[110, 1035], [265, 275], [910, 260],
                                        [1640, 915]])
        self.target_vertices = np.array([[0, court_width], [0, 0],
                                         [court_length, 0],
                                         [court_length, court_width]])
        self.pixel_vertices = self.pixel_vertices.astype(np.float32)
        self.target_vertices = self.target_vertices.astype(np.float32)
        self.persepctive_trasnformer = cv2.getPerspectiveTransform(
            self.pixel_vertices, self.target_vertices)

    def transform_point(self, point):
        p = (int(point[0]), int(point[1]))
        is_inside = cv2.pointPolygonTest(self.pixel_vertices, p, False) >= 0
        if not is_inside:
            return
        reshaped_point = point.reshape(-1, 1, 2).astype(np.float32)
        tranform_point = cv2.perspectiveTransform(reshaped_point,
                                                  self.persepctive_trasnformer)
        return tranform_point.reshape(-1, 2)

    def add_transformed_position_to_tracks(self, tracks):
        for object, object_tracks in tracks.items():
            for frame_num, track in enumerate(object_tracks):
                for track_id, track_info in track.items():
                    position = track_info["position_adjusted"]
                    position = np.array(position)
                    position_trasnformed = self.transform_point(position)
                    if position_trasnformed is not None:
                        position_trasnformed = position_trasnformed.squeeze(
                        ).tolist()
                    tracks[object][frame_num][track_id][
                        "position_transformed"] = position_trasnformed
