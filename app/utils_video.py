import cv2

camera = cv2.VideoCapture(0)
'''
for ip camera use - 
rtsp://username:password@ip_address:554/
user=username_password='password'_channel=channel_number_stream=0.sdp' 

for local webcam use cv2.VideoCapture(0)
'''


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
