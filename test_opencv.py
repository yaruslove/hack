import cv2
import os

print(os.listdir("/saved_video"))

def video_resolution(path_video):
    vcap = cv2.VideoCapture(path_video) # , cv2.CAP_GSTREAMER
    print(f"vcap {vcap}")
    print(vcap.isOpened())
    if vcap.isOpened(): 
        height = int(vcap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float `height`
        width  = int(vcap.get(cv2.CAP_PROP_FRAME_WIDTH))   # float `width`
    else:
        print(f"video_can't open")
    vcap.release()
    return ( width, height)

path_video = "/saved_video/video_2.mp4"
size = video_resolution(path_video)
print(f"well done size = {size}")

# print (os.listdir("/hack/saved_data/"))
