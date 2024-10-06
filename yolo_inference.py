from ultralytics import YOLO

# model = YOLO('yolov8x')

# results = model.predict('input_videos/WhatsApp Video 2024-08-26 at 19.20.06_33ee2ee1.mp4',save=True)
 
# print(results[0])

# print('=======================================================================')
# for box in results[0].boxes:
#     print(box)
        
# !pip install roboflow  


model = YOLO('models/best.pt')

results = model.predict('input_videos/WhatsApp Video 2024-08-26 at 19.20.06_33ee2ee1.mp4',save=True)
 
print(results[0])

print('=======================================================================')
for box in results[0].boxes:
    print(box)
        