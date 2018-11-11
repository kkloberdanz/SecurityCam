import cv2
import io
import time


def stream():
    start = time.time()
    try:
        cap = cv2.VideoCapture(0)
        while(True):
            # Capture frame-by-frame
            ret, frame = cap.read()
            _, jpg = cv2.imencode('.jpg', frame)
            yield jpg.tobytes()
            if time.time() - start > 600: # 10 minute timeout
                raise Exception('End of stream')
            time.sleep(0.05) # limit frame-rate to <24 FPS

    except Exception as e:
        pic = cv2.imread('end_of_stream.jpg')
        _, jpg = cv2.imencode('.jpg', pic)
        print(e)
        yield jpg.tobytes()

    finally:
        cap.release()
