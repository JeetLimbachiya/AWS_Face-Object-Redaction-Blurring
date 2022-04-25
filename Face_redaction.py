# importing the necessary packages
import argparse                         # to pass arguments
import cv2                              # requires 'opencv-contrib-python==3.4.x.x'
#import os
#import boto3
from datetime import datetime

#cli = boto3.client('s3')
#res = boto3.resource('s3')

class FaceBlur:
    def __init__(self):
        # construct the argument parser and parse the arguments
        self.ap = argparse.ArgumentParser()
        self.ap.add_argument("-v", "--video", type=str,
                        help="path to input video file")
        self.ap.add_argument("-t", "--tracker", type=str, default="kcf",
                        help="OpenCV object tracker type")

        self.args = vars(self.ap.parse_args())

        # initialize a dictionary that maps strings to their corresponding
        # OpenCV object tracker implementations
        self.__OPENCV_OBJECT_TRACKERS = {
            "csrt": cv2.TrackerCSRT_create,
            "kcf": cv2.TrackerKCF_create,
            "boosting": cv2.TrackerBoosting_create,
            "mil": cv2.TrackerMIL_create,
            "tld": cv2.TrackerTLD_create,
            "medianflow": cv2.TrackerMedianFlow_create,
            "mosse": cv2.TrackerMOSSE_create
        }

        # initialize OpenCV's special multi-object tracker
        self.trackers = cv2.MultiTracker_create()

        # self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.fourcc = cv2.VideoWriter_fourcc(*'MP4V')

        # self.out = cv2.VideoWriter('Output.avi', self.fourcc, 30, (1800, 1000))
        self.out = cv2.VideoWriter('Output.mp4', self.fourcc, 30, (1800, 1000))

    def main(self):
        # if a video path was not supplied, grab the reference to the web cam
        if not self.args.get("video"):
            print("[INFO] starting video stream...")
            vs = cv2.VideoCapture(0)

        # otherwise, grab a reference to the video file
        else:
            vs = cv2.VideoCapture(self.args["video"])

        # loop over frames from the video stream
        while True:
            # grab the current frame, then handle if we are using a VideoStream or VideoCapture object
            ret, frame = vs.read()

            # check to see if we have reached the end of the stream
            if ret is None:
                vs = cv2.VideoCapture(self.args["video"])
                ret, frame = vs.read()
                continue

            # resize the  frame (so we can process it faster)
            if ret:
                timer = cv2.getTickCount()
                frame = cv2.resize(frame, (1800, 1000))             # (width, height)

                # grab the updated bounding box coordinates (if any) for each object that is being tracked
                (success, boxes) = self.trackers.update(frame)

                # loop over the bounding boxes and draw then on the frame
                for box in boxes:
                    (x, y, w, h) = [int(v) for v in box]

                    frame[y:y + h, x:x + w] = cv2.GaussianBlur(src=frame[y:y + h, x:x + w], ksize=(33, 33), sigmaX=22)  # higher ksize, sigmaX == higher blur intensity
                    # Note: 'ksize' should always be Odd Number

                # Display FPS
                cv2.rectangle(frame, pt1=(50, 20), pt2=(220, 60), color=(0, 0, 0), thickness=-1)
                fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
                cv2.putText(frame, f'FPS: {str(int(fps))}', (60, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)

                key = cv2.waitKey(1) & 0xFF

                # if the 'c' key is selected, the frame will be paused and we are going to "capture" a bounding box to track
                if key == ord("c"):
                    # select the bounding box of the object we want to track (make
                    # select the bounding box of the object we want to track (make
                    # sure you press ENTER or SPACE after selecting the ROI)
                    box = cv2.selectROI("Frame", frame, fromCenter=False, showCrosshair=True)

                    # create a new object tracker for the bounding box and add it to our multi-object tracker
                    tracker = self.__OPENCV_OBJECT_TRACKERS[self.args["tracker"]]()
                    self.trackers.add(tracker, frame, box)
                 # if the `q` key was pressed, break from the loop
                elif key == ord("q"):
                    break

            # write the frames to the video file
            self.out.write(frame)

            # show the frames
            cv2.imshow("Frame", frame)

            #data_file_folder = '/home/ubuntu/Ash_FaceRedaction'
            #for file in os.listdir(data_file_folder):
            #    if file.endswith(".mp4"):
            #        cli.upload_file(Filename='/home/ubuntu/Ash_FaceRedaction/Output.mp4', Bucket='fbwithoutbucket',Key=file)

            # res.Bucket('fbwithoutbucket').upload_file('/home/ubuntu/Ash_FaceRedaction/Output.mp4','Output.mp4')



        # if we are using a webcam, release the pointer
        if not self.args.get("video", False):
            vs = cv2.VideoCapture(self.args["video"])
            ret, frame = vs.read()

        # otherwise, release the file pointer
        else:
            vs.release()

    # close all windows
    cv2.destroyAllWindows()


fb = FaceBlur()                     # Initializing class
fb.main()                           # Caling main function