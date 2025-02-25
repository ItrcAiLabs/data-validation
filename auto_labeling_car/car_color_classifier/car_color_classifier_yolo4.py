import numpy as np
import time
import cv2
import os
from  .classifier import Classifier

def detect_car_color(image_path, yolo_path='./car_color_classifier/yolov4', confidence_threshold=0.5, nms_threshold=0.3):
    car_color_classifier = Classifier()
    
    # Load YOLO class labels
    labelsPath = os.path.sep.join([yolo_path, "coco.names"])
    LABELS = open(labelsPath).read().strip().split("\n")
    
    # Load YOLO model
    weightsPath = os.path.sep.join([yolo_path, "yolov4.weights"])
    configPath = os.path.sep.join([yolo_path, "yolov4.cfg"])
    net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
    
    # Load input image
    image = cv2.imread(image_path)
    (H, W) = image.shape[:2]
    
    # Get YOLO output layer names
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]
    
    # Convert image to blob and perform forward pass
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (608, 608), swapRB=True, crop=False)
    net.setInput(blob)
    outputs = net.forward(output_layers)
    
    # Initialize bounding box lists
    boxes, confidences, classIDs = [], [], []
    
    # Process detections
    for output in outputs:
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]
            
            if confidence > confidence_threshold:
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")
                x, y = int(centerX - (width / 2)), int(centerY - (height / 2))
                
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)
    
    # Apply non-maxima suppression
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, confidence_threshold, nms_threshold)
    
    # Process detections
    if len(idxs) > 0:
        for i in idxs.flatten():
            if classIDs[i] == 2:  # Class ID 2 corresponds to 'car'
                x, y, w, h = boxes[i]
                car_crop = image[max(y, 0):y + h, max(x, 0):x + w]
                
                # Predict car color
                result = car_color_classifier.predict(car_crop)
                return result[0]['color']
    
    return "No car detected"

# Example usage:
# color = detect_car_color("test.jpg")
# print("Detected Car Color:", color)
