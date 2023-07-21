#import
import cv2
from os.path import basename
from tqdm import tqdm


#class
class MP4Converter:
    def __init__(self, filepath) -> None:
        self.capture = cv2.VideoCapture(filepath)
        fps = self.capture.get(cv2.CAP_PROP_FPS)
        height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.writer = cv2.VideoWriter(f'{basename(filepath)[:-3]}mp4',
                                      cv2.VideoWriter_fourcc(*'mp4v'), fps,
                                      (width, height))

    def __call__(self):
        pbar = tqdm()
        while self.capture.isOpened():
            pbar.update(1)
            ret, img = self.capture.read()
            if ret:
                self.writer.write(img)
            else:
                break
        self.capture.release()
        self.writer.release()


if __name__ == '__main__':
    #parameters
    filepath = 'test.mov'

    #create converter
    converter = MP4Converter(filepath=filepath)

    #run
    converter()