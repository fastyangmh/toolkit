# import
import torch

# def


def label_smoothing(one_hot, alpha, num_classes):
    return one_hot*(1-alpha)+(alpha/num_classes)


if __name__ == '__main__':
    # parameters
    num_classes = 3
    num_labels = 5
    alpha = 0.1

    # create labels
    labels = torch.randint(0, num_classes, size=(num_labels,))
    one_hot_labels = torch.eye(num_classes)[labels]

    # smoth labels
    one_hot_labels_smoothed = label_smoothing(
        one_hot=one_hot_labels, alpha=alpha, num_classes=num_classes)

    # display result
    print('original: \n{}'.format(one_hot_labels))
    print('smoothed: \n{}'.format(one_hot_labels_smoothed))
