#import
from torch.utils.data import Dataset
from sklearn.datasets import load_breast_cancer
from typing import TypeVar

T_co = TypeVar('T_co', covariant=True)


#class
class MyBreastCancerDataset(Dataset):
    # NOTE: this dataset contains only training and validation datasets and the training and validation of ratio is 8:2
    def __init__(self, train, transform, target_transform) -> None:
        super().__init__()
        self.data = load_breast_cancer().data
        self.targets = load_breast_cancer().target
        self.classes = list(load_breast_cancer().target_names)
        self.class_to_idx = {k: v for v, k in enumerate(self.classes)}
        l = len(self.data)
        if train:
            self.data = self.data[:int(l * 0.8)]
            self.targets = self.targets[:int(l * 0.8)]
        else:
            self.data = self.data[int(l * 0.8):]
            self.targets = self.targets[int(l * 0.8):]
        self.transform = transform
        self.target_transform = target_transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index) -> T_co:
        sample = self.data[index]
        target = self.targets[index]
        if self.transform is not None:
            sample = self.transform(sample)
        if self.target_transform is not None:
            target = self.target_transform(target)
        return sample, target


if __name__ == '__main__':
    #parameters
    transform = None
    target_transform = None

    #create training and validation dataset
    train_dataset = MyBreastCancerDataset(train=True,
                                          transform=transform,
                                          target_transform=target_transform)
    val_dataset = MyBreastCancerDataset(train=False,
                                        transform=transform,
                                        target_transform=target_transform)

    #display the information of dataset
    print(f'the length of training dataset: {len(train_dataset)}')
    print(f'the length of validation dataset: {len(val_dataset)}')

    #get the first sample and target in training dataset
    x, y = train_dataset[0]

    #display the dimension of sample and target
    print(f'the dimension of sample: {x.shape}')
    print(f'the dimension of target: {1 if y.shape==() else y.shape}')
