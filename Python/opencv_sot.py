#import
import cv2
from tqdm import tqdm
from os.path import join

if __name__ == '__main__':
    #parameters
    filepath = 'video.mp4'
    tracker = None
    model_root = '../resource/DaSiamRPN/'

    #create video capture
    video_capture = cv2.VideoCapture(filepath)

    #run
    pbar = tqdm()
    while video_capture.isOpened():
        pbar.update(1)
        ret, frame = video_capture.read()
        if ret:
            if tracker is None:
                frame = cv2.putText(
                    img=frame,
                    text='Select a ROI and then press SPACE or ENTER button!',
                    org=(10, 15),
                    fontFace=cv2.FONT_HERSHEY_COMPLEX,
                    color=(0, 0, 255),
                    thickness=1,
                    fontScale=0.5)
                frame = cv2.putText(
                    img=frame,
                    text='Cancel the selection process by pressing c button!',
                    org=(10, 30),
                    fontFace=cv2.FONT_HERSHEY_COMPLEX,
                    color=(0, 0, 255),
                    thickness=1,
                    fontScale=0.5)
                bbox = cv2.selectROI(windowName='frame', img=frame)
                if sum(bbox):
                    params = cv2.TrackerDaSiamRPN_Params()
                    params.kernel_cls1 = join(model_root, params.kernel_cls1)
                    params.kernel_r1 = join(model_root, params.kernel_r1)
                    params.model = join(model_root, params.model)
                    xyxy = [
                        bbox[0], bbox[1], bbox[0] + bbox[2], bbox[1] + bbox[3]
                    ]
                    tracker = cv2.TrackerDaSiamRPN_create(parameters=params)
                    tracker.init(frame, bbox)
            else:
                track_status, bbox = tracker.update(frame)
                if track_status:
                    xyxy = [
                        bbox[0], bbox[1], bbox[0] + bbox[2], bbox[1] + bbox[3]
                    ]
                    frame = cv2.rectangle(img=frame,
                                          pt1=xyxy[:2],
                                          pt2=xyxy[2:],
                                          color=(0, 0, 255),
                                          thickness=2)
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) == ord('q'):
                break
        else:
            break
    video_capture.release()