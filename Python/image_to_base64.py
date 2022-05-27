#import
from PIL import Image
from io import BytesIO
import base64


#def
def image_to_base64(image):
    buffer = BytesIO()
    image.save(fp=buffer, format='png')
    byte = buffer.getvalue()
    return base64.b64encode(s=byte)


if __name__ == '__main__':
    #parameters
    filepath = 'image.jpg'

    #load image
    image = Image.open(fp=filepath)

    #convert image to base64
    encoded = image_to_base64(image=image)

    #display
    print(encoded)