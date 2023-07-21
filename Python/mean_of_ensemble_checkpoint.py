#import
from os.path import join
from glob import glob
import torch
from tqdm import tqdm
from collections import OrderedDict


#def
def mean_of_ensemble_checkpoint(files, device, save_path):
    #load checkpoints and sum of model weight
    state_dict = OrderedDict()
    for f in tqdm(files):
        checkpoint = torch.load(f, map_location=device)
        checkpoint = {'state_dict': checkpoint['state_dict']}
        for k, v in checkpoint['state_dict'].items():
            if k in state_dict:
                state_dict[k] += v
            else:
                state_dict[k] = v

    #calculate mean
    for k, v in state_dict.items():
        state_dict[k] = v / len(files)

    #save checkpoint
    checkpoint = {'state_dict': state_dict}
    torch.save(obj=checkpoint, f=save_path)


if __name__ == '__main__':
    #parameters
    root = 'checkpoints/'
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    save_path = 'mean_of_ensemble_model_weight.ckpt'

    #find ckpts
    files = glob(pathname=join(root, '*.ckpt'))

    #calculate
    mean_of_ensemble_checkpoint(files=files,
                                device=device,
                                save_path=save_path)
