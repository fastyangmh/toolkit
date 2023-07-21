#import
import cv2
import zmq
from tqdm import tqdm
from time import time

if __name__ == '__main__':
    #parameters

    #create cap
    cap = cv2.VideoCapture(0)

    #create zmq
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.set_hwm(1)

    #bind port
    socket.bind(f"ipc:///tmp/zmqtest")

    #run
    pbar = tqdm()
    while cap.isOpened():
        pbar.update(1)
        ret, frame = cap.read()
        meta_data = None
        if ret:
            height, width, channel = frame.shape
            frame_bytes = frame.tobytes()
            meta_data = {
                "height": str(height),
                "width": str(width),
                "channel": str(channel),
                "timestamp": str(time()),
            }
            socket.send_json(meta_data, zmq.SNDMORE)
            socket.send(frame_bytes, copy=False, track=False)