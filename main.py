from models.model_architecture import model
from sklearn import preprocessing
import pandas as pd
import mediapipe as mp
from utils import *




def generate_video():


    ################################################### VARIABLES INITIALIZATION ###########################################################

    # Set to normal mode (=> no recording of data)
    first_keyword = []
    keywords = []
    mode = 0

    CSV_PATH = 'data/keypoint.csv'

    # Camera settings
    WIDTH = 2158//2
    HEIGHT = 1520//2

    cap = cv.VideoCapture(0)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, HEIGHT)

    # important keypoints (wrist + tips coordinates)
    # for training the model
    RIGHTHAND_TRAINING_KEYPOINTS = [keypoint for keypoint in range(0, 21, 4)]
    LEFTHAND_TRAINING_KEYPOINTS = [keypoint for keypoint in range(0, 21, 4)]

    # Hand and pose detector
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.75)

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    # Hand landmarks drawing
    mp_drawing = mp.solutions.drawing_utils

    # Load saved model for hand gesture
    GESTURE_RECOGNIZER_PATH = 'models/model.pth'
    model.load_state_dict(torch.load(GESTURE_RECOGNIZER_PATH))

    # Load Label
    LABEL_PATH = 'data/label.csv'
    labels = pd.read_csv(LABEL_PATH, header=None).values.flatten().tolist()

    # confidence threshold(required to translate gestures into commands)
    CONF_THRESH = 0.9



    ################################################### INITIALIZATION END ###########################################################


    while True:
        #key = cv.waitKey(1)
        # if key == ord('q'):
        #     break

        # choose mode (normal or recording)
        mode = select_mode(mode=mode)
        print(f'mode:{mode}')

        # class id for recording
        #class_id = get_class_id(key)
        #print(f'class:{class_id}, key:{key}, mode:{mode}')

        # read camera
        has_frame, frame = cap.read()
        if not has_frame:
            break

        # horizontal flip and color conversion for mediapipe
        frame = cv.flip(frame, 1)
        frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)



    ############################################ GESTURE DETECTION / TRAINING POINT LOGGING ###########################################################
        
        
        
        result = hands.process(frame_rgb)
        results = pose.process(frame_rgb)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:

                # draw landmarks
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                #mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                # Get coordinates
                leftshoulder = [results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                leftelbow = [results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                leftwrist = [results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST.value].x,results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                rightshoulder = [results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                rightelbow = [results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                rightwrist = [results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]


                # Calculate angle
                leftangle = calculate_angle(leftshoulder, leftelbow, leftwrist)
                angles = np.array(leftangle).reshape(-1, 1)
                leftnormalize_pose = preprocessing.normalize(angles)
                leftnormalize = np.squeeze(leftnormalize_pose, 0)
                #print(leftnormalize)

                rightangle = calculate_angle(rightshoulder, rightelbow, rightwrist)
                angle = np.array(rightangle).reshape(-1, 1)
                rightnormalize_pose = preprocessing.normalize(angle)
                rightnormalize = np.squeeze(rightnormalize_pose, 0)
            

                # get landmarks coordinates
                coordinates_list = calc_landmark_coordinates(frame_rgb, hand_landmarks)
                rh_important_points = [coordinates_list[i] for i in RIGHTHAND_TRAINING_KEYPOINTS]
                lh_important_points = [coordinates_list[i] for i in LEFTHAND_TRAINING_KEYPOINTS]

                # Conversion to relative coordinates and normalized coordinates
                rh_preprocessed = pre_process_landmark(rh_important_points)
                lh_preprocessed = pre_process_landmark(lh_important_points)
                
                # compute the needed distances to add as to coordinates features
                d0 = calc_distance(coordinates_list[0], coordinates_list[5])
                rh_pts_for_distances = [coordinates_list[i] for i in [4, 8, 12, 16, 20]]
                rh_distances = normalize_distances(d0, get_all_distances(rh_pts_for_distances)) 

                lh_pts_for_distances = [coordinates_list[i] for i in [4, 8, 12, 16, 20]]
                lh_distances = normalize_distances(d0, get_all_distances(lh_pts_for_distances)) 
                
                # Write to the csv file "keypoint.csv"(if mode == 1)
                # logging_csv(class_id, mode, preprocessed)
                features = np.concatenate([rh_preprocessed,  lh_preprocessed, rh_distances, lh_distances, leftnormalize, rightnormalize])
                #logging_csv(class_id, mode, features, CSV_PATH)



                # inference
                conf, pred = predict(features, model)
                gesture = labels[pred]



    ############################################  PREDTICTON / NLP / AUDIO   ###########################################################


                if conf > CONF_THRESH :    
                    color = (245, 242, 226)
                    cv.circle(frame, (70, 70), 15, color, -1)   
                    first_keyword.append(gesture)
                    [keywords.append(rem_extra) for rem_extra in first_keyword if rem_extra not in keywords]
                    print(keywords)
            

        
        sentences = text(frame, mode, words = keywords, params= {"do_sample":False, "num_beams":4, "no_repeat_ngram_size":3, "early_stopping":True})


        # show detected gesture
        cv.rectangle(frame, (0,0), (640, 40), (245, 117, 16), -1)
                            
        cv.putText(frame, ' '.join(sentences), (3,30), 
                                cv.FONT_HERSHEY_COMPLEX_SMALL, 0.7, (255, 255, 255), 1, cv.LINE_AA)

    
        del_text(mode, keywords=keywords, first_keyword=first_keyword)
        #draw_info(frame, mode, class_id)


        _ , buffer = cv.imencode('.jpg', frame)
        frame  = buffer.tobytes()
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


    cap.release()
    cv.destroyAllWindows()