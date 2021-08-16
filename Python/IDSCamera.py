'''
https://cn.ids-imaging.com/manuals/ids-software-suite/ueye-manual/4.94/zh/is_camerastatus.html
'''

# import
import configparser
from pyueye import ueye
from ctypes import c_uint, c_wchar_p
import numpy as np
import matplotlib.pyplot as plt
from os.path import isfile
import cv2

# class


class IDSCamera:
    def __init__(self, camera_parameter_path):
        # table
        self.color_modes_table = {'6': 'ueye.IS_CM_MONO8',
                                  '0': 'ueye.IS_CM_BGRA8_PACKED',
                                  '1': 'ueye.IS_CM_BGR8_PACKED'}
        self.bits_of_pixel_table = {'6': 8,
                                    '0': 32,
                                    '1': 24}
        self.color_code_table = {'BGR': cv2.COLOR_BGR2RGB,
                                 'BGRA': cv2.COLOR_BGRA2RGB}

        # parameters
        self.config = self._load_ini_file(
            camera_parameter_path=camera_parameter_path)
        self.width = int(self.config['Image size']['Width'])
        self.height = int(self.config['Image size']['Height'])
        self.bitspixel = self.bits_of_pixel_table[self.config['Parameters']['Colormode']]
        self.lineinc = self.width * int((self.bitspixel + 7) / 8)
        self.channels = int(np.ceil((self.bitspixel/8)))
        self.color_mode = self.color_modes_table[self.config['Parameters']['Colormode']]
        self.color_order = ''.join(filter(lambda x: not x.isdigit(
        ), self.color_mode.split('IS_CM_')[1].split('_')[0]))
        self.color_code = self.color_code_table.get(self.color_order)

        # init camera
        self.camera = ueye.HIDS(0)
        result = ueye.is_InitCamera(phCam=self.camera, hWnd=None)
        self._check(result=result, info='initial')

        # set color mode
        result = ueye.is_SetColorMode(
            hCam=self.camera, Mode=eval(self.color_mode))
        self._check(result=result, info='set color mode')

        # load parameter
        result = ueye.is_ParameterSet(hCam=self.camera, nCommand=ueye.IS_PARAMETERSET_CMD_LOAD_FILE, pParam=c_wchar_p(
            camera_parameter_path), cbSizeOfParam=c_uint(0))
        self._check(result=result, info='load parameter')

        # allocate memory
        self.mem_ptr = ueye.c_mem_p()
        mem_id = ueye.int()
        result = ueye.is_AllocImageMem(hCam=self.camera, width=self.width, height=self.height,
                                       bitspixel=self.bitspixel, ppcImgMem=self.mem_ptr, pid=mem_id)
        self._check(result=result, info='allocate memory')

        # set active memory region
        result = ueye.is_SetImageMem(
            hCam=self.camera, pcMem=self.mem_ptr, id=mem_id)
        self._check(result=result, info='set active memory region')

        # set DIB
        result = ueye.is_SetDisplayMode(
            hCam=self.camera, Mode=ueye.IS_SET_DM_DIB)
        self._check(result=result, info='set DIB')

    def _load_ini_file(self, camera_parameter_path):
        config = configparser.ConfigParser()
        config.read(camera_parameter_path, 'utf-8-sig')
        return config

    def _check(self, result, info):
        assert result == ueye.IS_SUCCESS, 'the camera does not successful {}, the return code {}.'.format(
            info, result)

    def __call__(self):
        result = ueye.is_FreezeVideo(hCam=self.camera, Wait=ueye.IS_WAIT)
        self._check(result=result, info='freeze video')
        image = ueye.get_data(image_mem=self.mem_ptr, x=self.width, y=self.height,
                              bits=self.bitspixel, pitch=self.lineinc, copy=False)
        if self.channels > 1:
            image = np.reshape(a=image, newshape=(
                self.height, self.width, self.channels))
            image = cv2.cvtColor(src=image, code=self.color_code)
            image = np.array(image)
        else:
            image = np.reshape(a=image, newshape=(self.height, self.width))
        return image

    def release(self):
        result = ueye.is_ExitCamera(hCam=self.camera)
        self._check(result=result, info='exit camera')


if __name__ == '__main__':
    # parameters
    camera_parameter_path = 'parameters.ini'

    # check camera parameter file
    assert isfile(
        path=camera_parameter_path), 'the camera parameters does not exist.'

    # initialize camera
    camera = IDSCamera(camera_parameter_path=camera_parameter_path)

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
