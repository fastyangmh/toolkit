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

# class


class IDSCAMERA:
    def __init__(self, camera_parameter_path):
        # parameters
        self.color_mode = {'6': 'ueye.IS_CM_MONO8',
                           '0': 'ueye.IS_CM_BGRA8_PACKED'}
        self.bits_of_pixel = {'6': 8,
                              '0': 32}
        self.config = self._load_ini_file(
            camera_parameter_path=camera_parameter_path)
        self.width = int(self.config['Image size']['Width'])
        self.height = int(self.config['Image size']['Height'])
        self.bitspixel = self.bits_of_pixel[self.config['Parameters']['Colormode']]
        self.lineinc = self.width * int((self.bitspixel + 7) / 8)
        self.channels = int(np.ceil((self.bitspixel/8)))

        # init camera
        self.camera = ueye.HIDS(0)
        result = ueye.is_InitCamera(
            phCam=self.camera, hWnd=None)
        self._check(result=result, info='initial')

        # set color mode
        result = ueye.is_SetColorMode(hCam=self.camera, Mode=eval(
            self.color_mode[self.config['Parameters']['Colormode']]))
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

    def _load_ini_file(self, camera_parameter_path):

        config = configparser.ConfigParser()
        config.read(camera_parameter_path, 'utf-8-sig')
        return config

    def _check(self, result, info):
        assert result == ueye.IS_SUCCESS, 'the camera does not successful {}, the return code {}.'.format(
            info, result)

    def __call__(self):
        result = ueye.is_FreezeVideo(hCam=self.camera, Wait=ueye.IS_DONT_WAIT)
        self._check(result=result, info='freeze video')
        image = ueye.get_data(image_mem=self.mem_ptr, x=self.width, y=self.height,
                              bits=self.bitspixel, pitch=self.lineinc, copy=False)
        if self.channels > 1:
            image = np.reshape(a=image, newshape=(
                self.height, self.width, self.channels))
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
    camera = IDSCAMERA(camera_parameter_path=camera_parameter_path)

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
