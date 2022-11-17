#!pip install keytotext -q


import csv
import cv2 as cv
import numpy as np
import torch
import time
import pyttsx3
from collections import deque
from keytotext import pipeline
import keyboard


nlp = pipeline("mrm8488/t5-base-finetuned-common_gen")



def select_mode(mode):
    """ Active either the normal mode (0 => nothing happens)
    or the recording mode (1 => saving data)
    Args:
        key (int): An integer value triggered by pressing 'n' (for normal mode) or 'r' (for recording mode)
        mode (int): The current mode
    Returns:
        int: The activated mode
    """
    # if key == ord('n'):
    #     mode = 0
    # if key == ord('r'):
    #     mode = 1
    # if key == ord('a'):  # append
    #     mode = 2
    # if key == ord('h'):   # audio and text
    #     mode = 3



    if keyboard.is_pressed("a"):
        mode = 0
    if keyboard.is_pressed("d"):  # append
        mode = 2
    if keyboard.is_pressed("s"):   # audio and text
        mode = 3

    return mode



def get_class_id(key):
    """ Maps pressed keys on keyboard to a class label that will
    associated to a given gesture.
    Args:
        key (int): A key on the keyboard
    Returns:
        int: A class id/label
    """
    class_id = -1

    if 48 <= key <= 57:  # numeric keys
        class_id = key - 48
    if 65 <= key <= 74:  # numeric keys
        class_id = key - 55
    return class_id



def logging_csv(class_id, mode, features, file_path):
    """ Records the gesture label together with features representing that gesture in a csv file.
    Args:
        class_id (int): The label corresponding to a given gesture
        mode (int): Activate the recording mode (1)
        features (Array): An array of numbers that maps to the gesture.
    """
    if mode == 0:
        pass
    if mode == 1 and (0 <= class_id <= 20):
        with open(file_path, 'a', newline="") as f:
            writer = csv.writer(f)
            writer.writerow([class_id, *features])



# Annotate frame
def draw_info(frame, mode, class_id):
    if mode == 1:
        cv.putText(frame, 'Logging Mode', (10, 90),
                cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1, cv.LINE_AA)

        if class_id != -1:
            cv.putText(frame, "Class ID:" + str(class_id), (10, 110),
                       cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1, cv.LINE_AA)  



# Extract x, y coordinates of the landmarks
def calc_landmark_coordinates(frame, landmarks):
    frame_height, frame_width = frame.shape[:2]

    landmark_coordinates = []

    # Keypoint
    for landmark in landmarks.landmark:
        landmark_x = int(landmark.x * frame_width)
        landmark_y = int(landmark.y * frame_height)

        landmark_coordinates.append([landmark_x, landmark_y])

    return landmark_coordinates



# preprocess coordinates
def pre_process_landmark(landmark_list):
    coordinates = np.array(landmark_list)

    # relative coordinates to wrist keypoints
    wrist_coordinates = coordinates[0]
    relatives = coordinates - wrist_coordinates

    # Convert back to 1D array
    flattened = relatives.flatten()

    # Normalize between (-1, 1), exclude wrist coordinates(always 0)
    max_value = np.abs(flattened).max()

    normalized = flattened[2:]/max_value
    
    return normalized


# prediction
def predict(landmarks, model):

    model.eval()
    with torch.no_grad():
        landmarks = torch.tensor(landmarks.reshape(1, -1), dtype=torch.float)
        confidence = model(landmarks)
    conf, pred = torch.max(confidence, dim=1)
    return conf.item(), pred.item()


def calc_distance(pt1, pt2):
    # compute euclidian distance between two points pt1 and pt2
    return np.linalg.norm(np.array(pt1) - np.array(pt2))


def get_all_distances(pts_list):
    # Compute all distances between pts in a given list (pts_list)
    pts = deque(pts_list)
    distances = deque()
    while len(pts) > 1:
        pt1 = pts.popleft()
        distances.extend( [calc_distance(pt1, pt2) for pt2 in pts] )
    return distances


def normalize_distances(d0, distances_list):
    # normalize distances in distances_list by d0
    return np.array(distances_list) / d0
   

def del_text(mode, keywords, first_keyword):
    
    if mode == 2:
        del keywords[:]
        del first_keyword[:]
       

def text(frame, mode, words, params ):

    sentence = []

    if  mode == 3:
        color = (25, 35, 240)
        cv.circle(frame, (70, 70), 15, color, -1)
         
        sentence.append(nlp(words, **params))
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[2].id)
        engine.say(sentence)
        engine.runAndWait()
        print(sentence) 
        time.sleep(1)

    return sentence           


def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 

