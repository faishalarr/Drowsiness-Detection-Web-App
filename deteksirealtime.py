import cv2
import numpy as np
import argparse
import time
import pygame


model = "runs/train/exp/weights/best.onnx"
img_w = 640
img_h = 640
classes_file= 'classes.txt'

def class_name():
    classes=[]
    file= open(classes_file,'r')
    while True:
        name=file.readline().strip('\n')
        classes.append(name)
        if not name:
            break
    return classes

def detection1(img, net, classes): 
    blob = cv2.dnn.blobFromImage(img, 1/255 , (img_w, img_h), swapRB=True, mean=(0,0,0), crop= False)
    
    net.setInput(blob)
    t1= time.time()
    outputs= net.forward(net.getUnconnectedOutLayersNames())
    t2= time.time()
    out= outputs[0]
    #print('Opencv dnn yolov5 inference time: ', t2- t1)
    # print(out.shape)
    n_detections= out.shape[1]
    height, width= img.shape[:2]
    x_scale= width/img_w
    y_scale= height/img_h
    conf_threshold= 0.7
    score_threshold= 0.5
    nms_threshold = 0.5

    class_ids=[]
    score=[]
    boxes=[]

    ngantuk_detected = False # Initialize the flag for ngantuk detection

    for i in range(n_detections):
        detect=out[0][i]
        confidence= detect[4]
        if confidence >= conf_threshold:
            class_score= detect[5:]
            class_id= np.argmax(class_score)
            if (class_score[class_id]> score_threshold):
                score.append(confidence)
                class_ids.append(class_id)
                x, y, w, h = detect[0], detect[1], detect[2], detect[3]
                left= int((x - w/2)* x_scale )
                top= int((y - h/2)*y_scale)
                width = int(w * x_scale)
                height = int( h*y_scale)
                box= np.array([left, top, width, height])
                boxes.append(box)
                
                # Check if ngantuk is detected
                if classes[class_id] == "kantuk":
                    ngantuk_detected = True

    indices = cv2.dnn.NMSBoxes(boxes, np.array(score), conf_threshold, nms_threshold)
    
    for i in indices:
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]

        left, top, width, height = boxes[i]
        cv2.rectangle(img, (left, top), (left + width, top + height), (0, 0, 255), 2)
        label = "{}:{:.2f}".format(classes[class_ids[i]], score[i])
        # Modify the label to include the confidence score
        # Format the score to display only 2 decimal places
        text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 1)
        dim, baseline = text_size[0], text_size[1]
        cv2.rectangle(img, (left, top - 20), (left + dim[0], top + dim[1] + baseline - 20), (0,0,0), cv2.FILLED)
        cv2.putText(img, label, (left, top + dim[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 0), 1, cv2.LINE_AA)

        crop = img[top + 2:top + height - 2,left + 2:left + width - 2].copy()
        cv2.imshow('Detected Faces', crop)
        cv2.namedWindow("Detected Faces");
        cv2.moveWindow("Detected Faces", 670, 520);
    
    if len(score) > 0:
        score_label = "Score: {:.2f}".format(sum(score)/len(score))
        cv2.putText(img, score_label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    
    height1 = int(img.shape[0] * (width_frame / img.shape[1]))
    dim1 = (width_frame, height1)
    img1 = cv2.resize(img, dim1, interpolation = cv2.INTER_AREA)
    cv2.imshow('Detection Info', img1)
    cv2.namedWindow("Detection Info");
    cv2.moveWindow("Detection Info", 630,0);
    # cv2.waitKey(0)

    if ngantuk_detected: # If ngantuk is detected, play a sound alert
        alert_sound.play()
        cv2.imwrite('result.jpg', img)

width_frame = 600
net = cv2.dnn.readNetFromONNX(model)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
classes = class_name()

# Initialize pygame
pygame.init()

# Load alert sound
alert_sound = pygame.mixer.Sound('alert.mp3')

cap1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    ret1, frame1 = cap1.read()
    frame1 = cv2.flip(frame1,1)
    
    height1 = int(frame1.shape[0] * (width_frame / frame1.shape[1]))
    dim1 = (width_frame, height1)
    img1 = cv2.resize(frame1, dim1, interpolation = cv2.INTER_AREA)

    cv2.imshow('Realtime Feed', img1)
    cv2.namedWindow("Realtime Feed");
    cv2.moveWindow("Realtime Feed", 0, 0);

    detection1(frame1, net, classes)

    keyVal = cv2.waitKey(1) & 0xFF
    
    if keyVal == 27:  
        break

cap1.release()

cv2.destroyAllWindows()

