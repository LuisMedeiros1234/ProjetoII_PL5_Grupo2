import av
import cv2
import numpy as np

from djitellopy import Tello

tello = Tello()
tello.connect()

def test_video_stream():
    try:
        container = av.open('udp://@0.0.0.0:11111')
        for frame in container.decode(video=0):
            img = frame.to_image()  # Convert frame to an image
            array = np.array(img)  # Convert to array for OpenCV
            cv2.imshow('Video', array)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cv2.destroyAllWindows()

test_video_stream()
