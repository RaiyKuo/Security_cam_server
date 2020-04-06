import sys
sys.path.append('/home/raiy/.local/lib/python3.7/site-packages')  # Path for import following libs

import cv2
import face_recognition
import numpy as np
from datetime import datetime
import time

def extractFaces(media_path, filename, output_path):
    cap = cv2.VideoCapture(media_path + filename)
    extracted, face_areas = [], []
    process_this_frame = True
    num_of_captured = 0

    while True:
        try:
            ret, frame = cap.read()
            #cv2.imshow(frame)
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        except:
            break
        rgb_small_frame = small_frame[:, :, ::-1]

        if process_this_frame:
            locations = face_recognition.face_locations(rgb_small_frame, number_of_times_to_upsample=3) # Only works when number_of_times_to_upsample = 3
            captured = face_recognition.face_encodings(rgb_small_frame, locations)
            for i, face in enumerate(captured):
                top, right, bottom, left = locations[i]
                area = (right-left)*(bottom-top)
                matches = face_recognition.compare_faces(extracted, face)
                if matches and any(matches):
                    face_distances = face_recognition.face_distance(extracted, face)
                    best = np.argmin(face_distances)
                    if matches[best] and area >= face_areas[best]:
                        extracted[best] = face
                        face_areas[best] = area
                        cv2.imwrite(output_path+ filename + '_' + str(best + 1) + '.jpg', frame[top*4:bottom*4, left*4:right*4]) # Save only the face
                        #cv2.imwrite(output_path+ filename + '_' + str(best + 1) + '.jpg', frame)                                # Save the whole frame
                else:
                    extracted.append(face)
                    face_areas.append(area)
                    num_of_captured += 1
                    cv2.imwrite(output_path + filename + '_' + str(num_of_captured) + '.jpg', frame[top*4:bottom*4, left*4:right*4])  # Save only the face
                    #cv2.imwrite(output_path+ filename + '_' + str(num_of_captured) + '.jpg', frame)                                  # Save the whole frame

        process_this_frame = not process_this_frame
    return len(extracted)
    

if __name__ == '__main__':
    media_path, filename, output_path = sys.argv[1:4]   
    #'/var/www/live/', 'android-04-Apr-20-13:52:31.flv', '/home/raiy/Desktop/face_test/results/'

    with open(output_path + 'extractFaces.log', 'a') as f:
        f.write(datetime.now().strftime("[%m-%d-%Y, %T]  "))
        f.write('Start with video = {}\n'.format(media_path+filename))
        results = extractFaces(media_path, filename, output_path)
        f.write(datetime.now().strftime("[%m-%d-%Y, %T]  "))
        f.write('Finished with {} extracted faces saved in {}\n'.format(results,  output_path))
