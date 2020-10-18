import cv2
from tensorflow import keras
from keras.models import load_model
from keras.preprocessing import image
import numpy as np

model = load_model('FINALENDMODEL.h5')

global count,status
count=1

class VideoCamera(object):
    def __init__(self):
        # capturing video
        self.video = cv2.VideoCapture("20201016_212633_1.mp4")

    def __del__(self):
        # releasing camera
        self.video.release()


    def get_frame(self):


        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (50, 50)
        fontScale = 1

        thickness = 2
        global status
        status=''
        color=(0,255,0)
        while (self.video.isOpened()):
            ret, frame = self.video.read()

            cv2.waitKey(10)
            frame = cv2.resize(frame, (224, 224))
            frame = frame[..., ::-1]
            global count
            count+=1
            if count%10==0:

                count=1
                x = image.img_to_array(frame)
                x = np.expand_dims(x, axis=0)
                images = np.vstack([x])
                classes = model.predict_classes(images, batch_size=1)
                print(classes)
                if classes[0][0]==0:
                    status="SAFE"
                    color = (255, 0, 0)
                else:
                    status="NOT SaFe"
                    color = (0, 0, 255)

            frame = frame[..., ::-1]
            frame = cv2.putText(frame, status, org, font,
                                            fontScale, color, thickness, cv2.LINE_AA)

            ret, jpeg = cv2.imencode('.jpeg', frame)

            return jpeg.tobytes()