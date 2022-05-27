#import
import numpy as np

if __name__ == '__main__':
    #parameters
    confusion_matrix = np.array([[9.22222e+06, 77080, 66978],
                                 [150462, 265618, 48786],
                                 [90975, 38635, 262861]])

    #calculate
    precision = np.diag(confusion_matrix) / np.sum(confusion_matrix, axis=0)
    recall = np.diag(confusion_matrix) / np.sum(confusion_matrix, axis=1)

    #check nan
    precision[np.isnan(precision)] = 0
    recall[np.isnan(recall)] = 0

    #display
    print(precision)
    print(recall)