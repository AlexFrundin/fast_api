import cv2

camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                continue
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                   bytearray(buffer) + b'\r\n')
    camera.release()
    cv2.destroyAllWindows()
