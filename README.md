# ⚽SPORTSIGHT

## Introduction
The goal of this project is to detect and track players, referees, and footballs in a video using YOLO, one of the best AI object detection models available. We will also train the model to improve its performance. Additionally, we will assign players to teams based on the colors of their t-shirts using Kmeans for pixel segmentation and clustering. With this information, we can measure a team's ball acquisition percentage in a match. We will also use optical flow to measure camera movement between frames, enabling us to accurately measure a player's movement. Furthermore, we will implement perspective transformation to represent the scene's depth and perspective, allowing us to measure a player's movement in meters rather than pixels. Finally, we will calculate a player's speed and the distance covered. This project covers various concepts and addresses real-world problems, making it suitable for both beginners and experienced machine learning engineers.

![Screenshot](output_videos/screenshot.png)

## Modules Used
The following modules are used in this project:
- YOLO: AI object detection model
- Kmeans: Pixel segmentation and clustering to detect t-shirt color
- Optical Flow: Measure camera movement
- Perspective Transformation: Represent scene depth and perspective
- Speed and distance calculation per player

## Trained Models
- [Trained Yolo v5](https://drive.google.com/file/d/1DC2kCygbBWUKheQ_9cFziCsYVSRw6axK/view?usp=sharing)

## Sample video
-  [Sample input video](https://drive.google.com/file/d/1t6agoqggZKx6thamUuPAIdN_1zR9v9S_/view?usp=sharing)

## Features

- **Object Detection**: Detect players, referees, and footballs using YOLOv8.
- **Custom Object Detector**: Fine-tune and train a custom YOLO model to improve detection accuracy.
- **Player Team Assignment**: Utilize KMeans clustering for pixel segmentation to accurately assign players to their respective teams based on t-shirt colors.
- **Camera Movement Measurement**: Implement optical flow techniques to measure camera movement between frames.
- **Perspective Transformation**: Use OpenCV's perspective transformation to represent scene depth and perspective, enabling accurate distance measurements in meters.
- **Speed and Distance Calculation**: Calculate players' speed and distance covered during the match.

## Datasets

- [Kaggle Dataset](https://www.kaggle.com/competitions/d...)
- [Video Link (Kaggle removed the videos)](https://drive.google.com/file/d/1t6ag...)
- [Roboflow Football Dataset](https://universe.roboflow.com/roboflo...)

## Requirements
To run this project, you need to have the following requirements installed:
- Python 3.x
- ultralytics
- supervision
- OpenCV
- NumPy
- Matplotlib
- Pandas

## Installation

To get started with SPORTSIGHT, clone this repository and install the required dependencies:

```bash
git clone https://github.com/yourusername/sportsight.git
