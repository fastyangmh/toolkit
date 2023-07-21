#import
from tqdm import tqdm
import zmq
import numpy as np
import cv2

if __name__ == '__main__':
    #parameters
    sleep_time = 1
    ZMQ_RECV_TIMEOUT = 1000  # ms

    #create zmq
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.setsockopt_string(zmq.SUBSCRIBE, '')
    socket.set_hwm(1)
    #socket.setsockopt(zmq.RCVTIMEO, ZMQ_RECV_TIMEOUT)

    #bind port
    socket.connect(f"ipc:///tmp/zmqtest")

    #run
    pbar = tqdm()
    while True:
        pbar.update(1)
        frame_meta = {}
        frame_meta = socket.recv_json()
        #print(frame_meta)
        height = frame_meta.get("height")
        width = frame_meta.get("width")
        channel = frame_meta.get("channel")
        frame = socket.recv()
        frame = np.ndarray((int(height), int(width), int(channel)),
                           dtype=np.uint8,
                           buffer=frame)
        #print(frame.shape)
        cv2.imshow('frame', frame)
        if cv2.waitKey(5) & 0xFF == 27:
            break