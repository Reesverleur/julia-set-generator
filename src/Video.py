# importing libraries
import os
import cv2
from PIL import Image

# Video Generating function
def generate_video():
    video_name = 'julia -2i to 2i.mp4'
    images = [img for img in os.listdir() if img.endswith(".jpg") or img.endswith(".jpeg") or img.endswith(".png")]
    
    print(images)
   
    frame = cv2.imread(images[0])
       
   	# setting the frame width, height width
   	# the width, height of first image
    height, width, layers = frame.shape
       
    video = cv2.VideoWriter(video_name, 0, 10, (width, height))

	# Appending the images to the video one by one
    for image in images:
        video.write(cv2.imread(image))
    
    # Deallocating memories taken for window creation
    cv2.destroyAllWindows()
    video.release() # releasing the video generated
# Calling the generate_video function
generate_video()
