#import
import cv2

if __name__ == '__main__':
    #parameters
    url = ''
    filepath = 'demo.mp4'

    #create cap
    cap = cv2.VideoCapture(url)

    #get cap attributes
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    #create writer
    writer = cv2.VideoWriter(filepath, cv2.VideoWriter_fourcc(*'mp4v'), fps,
                             (width, height))

    #run
    while cap.isOpened():
        ret, img = cap.read()
        if ret:
            writer.write(img)
            cv2.imshow('', img)
            if cv2.waitKey(1) == 'q':
                break
        else:
            break
    cap.release()