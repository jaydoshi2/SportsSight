# uncompyle6 version 3.9.2
# Python bytecode version base 3.8.0 (3413)
# Decompiled from: Python 3.8.10 (tags/v3.8.10:3d8993a, May  3 2021, 11:48:03) [MSC v.1928 64 bit (AMD64)]
# Embedded file name: d:\SportsSight\player_ball_assigner\player_ball_assigner.py
# Compiled at: 2024-09-27 21:09:30
# Size of source mod 2**32: 2695 bytes
import sys
sys.path.append("../")
from utils import get_center_of_bbox, measure_distance

class PlayerBallAssigner:

    def __init__(self):
        self.max_player_ball_distance = 70

    def assign_ball_to_player(self, players, ball_bbox):
        """"Purpose: This line calculates the center position of the ball using the get_center_of_bbox function,
        which likely takes a bounding box defined by coordinates (x1, y1, x2, y2) and returns a tuple (center_x, center_y)."""
        ball_position = get_center_of_bbox(ball_bbox)
        miniumum_distance = 99999
        assigned_player = -1
        for player_id, player in players.items():
            player_bbox = player["bbox"]
            distance_left = measure_distance((player_bbox[0], player_bbox[-1]), ball_position)
            distance_right = measure_distance((player_bbox[2], player_bbox[-1]), ball_position)
            distance = min(distance_left, distance_right)
            if distance < self.max_player_ball_distance and distance < miniumum_distance:
                miniumum_distance = distance
                assigned_player = player_id
            return assigned_player
