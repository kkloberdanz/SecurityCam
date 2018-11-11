import cv2
import time
import redis


redis_conn = redis.Redis(host='127.0.0.1',
                         port='6379')


def stream():
    start = time.time()
    try:
        while True:
            pic = redis_conn.get('current_frame')
            yield pic
            if time.time() - start > 600:  # 10 minute timeout
                raise Exception('End of stream')
            time.sleep(0.05)  # limit frame-rate to <24 FPS

    except Exception as e:
        pic = cv2.imread('end_of_stream.jpg')
        _, jpg = cv2.imencode('.jpg', pic)
        print(e)
        yield jpg.tobytes()


def capture():
    try:
        cap = cv2.VideoCapture(0)
        while(True):
            # Capture frame-by-frame
            ret, frame = cap.read()
            _, jpg = cv2.imencode('.jpg', frame)
            yield jpg.tobytes()

    finally:
        cap.release()


def record():
    for frame in capture():
        redis_conn.set('current_frame', frame)
        time.sleep(0.01)
