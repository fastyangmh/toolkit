'''
the following link is online manuals from IDS
https://cn.ids-imaging.com/manuals/ids-software-suite/ueye-manual/4.94/zh/sdk-programming-image-capture-modes.html
'''

# import
import configparser
from pyueye import ueye
import numpy as np
import matplotlib.pyplot as plt
from os.path import isfile
import cv2

# class


class IDSCamera:
    def __init__(self, parameter_path):
        # table
        self.color_mode_table = {
            '6': 'ueye.IS_CM_MONO8',
            '0': 'ueye.IS_CM_BGRA8_PACKED',
            '1': 'ueye.IS_CM_BGR8_PACKED'
        }
        self.bits_of_pixel_table = {'6': 8, '0': 32, '1': 24}
        self.color_code_table = {
            'BGR': cv2.COLOR_BGR2RGB,
            'BGRA': cv2.COLOR_BGRA2RGB
        }

        # get parameters from config
        self.config = self.load_ini_file(parameter_path=parameter_path)
        self.width = int(self.config['Image size']['Width'])
        self.height = int(self.config['Image size']['Height'])
        self.bitspixel = self.bits_of_pixel_table[self.config['Parameters']
                                                  ['Colormode']]
        self.lineinc = self.width * int((self.bitspixel + 7) / 8)
        self.channels = int(np.ceil((self.bitspixel / 8)))
        self.color_mode = self.color_mode_table[self.config['Parameters']
                                                ['Colormode']]
        self.color_order = ''.join(
            filter(lambda x: not x.isdigit(),
                   self.color_mode.split('IS_CM_')[1].split('_')[0]))
        self.color_code = self.color_code_table.get(self.color_order)

        # init camera
        self.camera = ueye.c_uint(
        )  #TODO: need to check if ueye.HIDS can select camera based on number
        self.hWnd = ueye.c_void_p()
        result = ueye.is_InitCamera(phCam=self.camera, hWnd=self.hWnd)
        self.check(result=result, info='is_InitCamera')

        # set color mode
        result = ueye.is_SetColorMode(hCam=self.camera,
                                      Mode=eval(self.color_mode))
        self.check(result=result, info='is_SetColorMode')

        # load parameter
        result = ueye.is_ParameterSet(
            hCam=self.camera,
            nCommand=ueye.IS_PARAMETERSET_CMD_LOAD_FILE,
            pParam=ueye.c_wchar_p(parameter_path),
            cbSizeOfParam=ueye.c_uint())
        self.check(result=result, info='is_ParameterSet')

        # allocate memory
        self.ppcMem = ueye.c_mem_p()
        self.pnMemId = ueye.c_int()
        result = ueye.is_AllocImageMem(hCam=self.camera,
                                       width=self.width,
                                       height=self.height,
                                       bitspixel=self.bitspixel,
                                       ppcMem=self.ppcMem,
                                       pnMemId=self.pnMemId)
        self.check(result=result, info='is_AllocImageMem')

        # set active memory region
        result = ueye.is_SetImageMem(hCam=self.camera,
                                     pcMem=self.ppcMem,
                                     nMemId=self.pnMemId)
        self.check(result=result, info='is_SetImageMem')

        # set DIB
        result = ueye.is_SetDisplayMode(hCam=self.camera,
                                        Mode=ueye.IS_SET_DM_DIB)
        self.check(result=result, info='is_SetDisplayMode')

    def load_ini_file(self, parameter_path):
        config = configparser.ConfigParser()
        config.read(parameter_path, 'utf-8-sig')
        return config

    def check(self, result, info):
        assert result == ueye.IS_SUCCESS, 'the camera does not successful {}, the return code is {}.'.format(
            info, result)

    def __call__(self):
        result = ueye.is_FreezeVideo(hCam=self.camera, Wait=ueye.IS_WAIT)
        self.check(result=result, info='is_FreezeVideo')
        image = ueye.get_data(image_mem=self.ppcMem,
                              x=self.width,
                              y=self.height,
                              bits=self.bitspixel,
                              pitch=self.lineinc,
                              copy=False)
        if self.channels > 1:
            image = np.reshape(a=image,
                               newshape=(self.height, self.width,
                                         self.channels))
            image = cv2.cvtColor(src=image, code=self.color_code)
            image = np.array(image)
        else:
            image = np.reshape(a=image, newshape=(self.height, self.width))
        return image

    def release(self):
        result = ueye.is_FreeImageMem(hCam=self.camera,
                                      pcMem=self.ppcMem,
                                      nMemId=self.pnMemId)
        self.check(result=result, info='is_FreeImageMem')
        result = ueye.is_ExitCamera(hCam=self.camera)
        self.check(result=result, info='is_ExitCamera')


if __name__ == '__main__':
    # parameters
    parameter_path = 'parameters.ini'

    # check camera parameter file
    assert isfile(path=parameter_path), 'the parameter does not exist.'

    # initialize camera
    camera = IDSCamera(parameter_path=parameter_path)

    # get image
    image = camera()

    # display image
    if camera.channels == 1:
        cmap = 'gray'
    else:
        cmap = None
    plt.imshow(image, cmap=cmap)
    plt.show()

    # release camera
    camera.release()
