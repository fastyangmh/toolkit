#import
import numpy as np


#def
def calculate_dice_score_by_class(classes, confusion_matrix):
    dice = {}
    for idx, c in enumerate(classes):
        TP = confusion_matrix[idx, idx]
        FP = np.sum(confusion_matrix[:, idx]) - TP
        FN = np.sum(confusion_matrix[idx, :]) - TP
        score = (2 * TP) / ((TP + FP) + (TP + FN))
        dice[c] = score
    return dice


if __name__ == '__main__':
    #parameters
    classes = ['background', 'benign', 'malignant']
    confusion_matrix = np.array([[3.72797e+07, 181827, 266520],
                                 [206064, 1.32302e+06, 23547],
                                 [176923, 19964, 1.41688e+06]])

    #calculate
    dice = calculate_dice_score_by_class(classes=classes,
                                         confusion_matrix=confusion_matrix)

    #display
    for k, v in dice.items():
        print(k, v)
