#import
from matplotlib import pyplot as plt
import numpy as np


#def
def rle2mask(mask_rle, shape):
    s = mask_rle.split()
    starts, lengths = [
        np.asarray(x, dtype=int) for x in (s[0:][::2], s[1:][::2])
    ]
    starts -= 1
    ends = starts + lengths
    img = np.zeros(shape[0] * shape[1], dtype=np.uint8)
    for lo, hi in zip(starts, ends):
        img[lo:hi] = 1
    return img.reshape(shape).T


if __name__ == '__main__':
    #parameters
    weight = 20
    height = 20
    rle = '2 3 7 2 10 5 17 7 25 1 29 1 32 1 34 4 40 1 42 1 45 1 48 2 51 1 54 1 56 1 58 1 60 1 62 1 64 3 68 4 73 3 79 1 81 4 87 1 89 1 91 3 95 1 98 1 100 1 105 1 108 1 111 1 115 1 121 2 125 2 130 1 133 3 137 5 143 2 146 6 154 3 159 1 161 5 169 1 171 2 176 2 179 1 182 1 185 1 188 2 191 1 194 1 197 6 204 3 208 1 210 1 212 1 214 3 218 2 224 4 229 1 231 2 237 1 240 2 243 1 246 2 249 1 252 8 264 4 269 3 273 1 275 1 279 1 281 1 283 1 285 1 287 1 289 1 291 1 294 2 299 1 301 1 304 1 307 2 315 3 319 6 328 3 332 2 335 1 338 1 341 1 343 6 350 1 352 1 354 1 357 1 361 1 366 3 371 2 375 2 379 1 381 3 385 2 390 1 394 2 397 1 399 1'

    #convert rle to mask
    mask = rle2mask(mask_rle=rle, shape=(weight, height))

    #display
    plt.imshow(mask)
    plt.show()