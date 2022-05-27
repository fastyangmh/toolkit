#import
import base64
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt


#def
def base64_to_image(encoded):
    byte = base64.b64decode(encoded)
    return Image.open(BytesIO(byte))


if __name__ == '__main__':
    #parameters
    encoded = b'iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAAAAABXZoBIAAAA70lEQVR4nMXQsWoCQRQF0JvBNNrGdjcgIR8gJJVrqRZCfkMkgn+QlEIIAcHaHzClVWySJkmXSgxqIbKCbcrLxRSbNe7M2uqr7syZefAecOTK9fTp78MLUs2ds9nJ+b71OPMfWzdXAALz9ZrSVCQpclp0bbiRpPVckmPlmUh268Ed2bDsfEVx2skCfsif9qkzxcsZAOCWYsHGDy+K/nuM2zmNuV5E6cQYc5/4+UDG0W07iTFfXlGhl45PJGelKGeQrOElgPFb8vJbqtWW0kYpG2qT8W7ZtdEP/zAcFbI2IniMsOkIAKD6zEGl6qXjweoXXfV/5XmKZEMAAAAASUVORK5CYII='

    #convert base64 to image
    image = base64_to_image(encoded=encoded)

    #display
    plt.imshow(X=image, cmap='gray')
    plt.show()