#import
import cv2
import mediapipe as mp

#global parameters
BODY_32_NAME_TO_INDEX = {
    k.name: k.value
    for k in mp.solutions.pose.PoseLandmark
}
BODY_32_INDEX_TO_NAME = {
    k.value: k.name
    for k in mp.solutions.pose.PoseLandmark
}

#class


class PoseEstimator:
    def __init__(self) -> None:
        self.model = mp.solutions.pose.Pose(static_image_mode=True,
                                            model_complexity=2,
                                            min_detection_confidence=0.5)

    def __call__(self, img):
        image_height, image_width, _ = img.shape
        results = self.model.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        pose_landmarks = results.pose_landmarks.landmark
        outputs = []
        for idx, v in enumerate(pose_landmarks):
            x = v.x if v.x <= 1.0 else 1.0
            y = v.y if v.y <= 1.0 else 1.0
            conf = v.visibility if v.visibility <= 1.0 else 1.0
            outputs.append([int(x * image_width), int(y * image_height), conf])
        return outputs


if __name__ == '__main__':
    #parameters
    filepath = 'pose.png'

    #load image
    img = cv2.imread(filepath)

    #create estimator
    estimator = PoseEstimator()

    #get outputs
    outputs = estimator(img=img)

    #display outputs
    print(outputs)