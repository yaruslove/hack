import cv2
from ultralytics import YOLO

import secrets

def get_id_hash(n):
    return secrets.token_urlsafe(n)

def count_fps(path_video):
    video = cv2.VideoCapture(path_video)
    # Find OpenCV version
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
    if int(major_ver)  < 3 :
        fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
        print ("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
    else :
        fps = video.get(cv2.CAP_PROP_FPS)
        print ("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))
    video.release()
    return fps

def video_resolution(path_video):
    vcap = cv2.VideoCapture(path_video)
    if vcap.isOpened(): 
        height = int(vcap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float `height`
        width  = int(vcap.get(cv2.CAP_PROP_FRAME_WIDTH))   # float `width`
    vcap.release()
    return ( width, height)

class Inference_video:
    def __init__ (self, weight_model):
        # Load the YOLOv8 model
        # weight_model = "/home/jovyan/tomato/script_2/app/best.pt"
        self.model = YOLO(weight_model) # 'yolov8n.pt'
        
    def inference_video(self,path_video, out_video_path):
        # Open the video file
        # path_video="/home/jovyan/tomato/script_2/data/in_video/video_2.mp4"
        # out_video_path ="/home/jovyan/tomato/script_2/data/out_video/video_2.mp4"

        cap = cv2.VideoCapture(path_video)

        #param in video
        size = video_resolution(path_video)
        fps = count_fps (path_video) 

        result = cv2.VideoWriter(out_video_path,  
                                 cv2.VideoWriter_fourcc(*'H264'), 
                                 fps, size) 

        # Loop through the video frames
        while cap.isOpened():
            # Read a frame from the video
            success, frame = cap.read()

            if success:
                # Run YOLOv8 inference on the frame
                results = self.model(frame)

                # Visualize the results on the frame
                annotated_frame = results[0].plot(line_width = 1, font_size = 0.5)

                ## write video
                result.write(annotated_frame)

                # Break the loop if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                # Break the loop if the end of the video is reached
                break


        # Release the video capture object and close the display window
        cap.release()
        result.release()
        cv2.destroyAllWindows()
        print(f"Finish well done work {path_video}!")
    