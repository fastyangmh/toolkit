# import
from pyueye import ueye
import tkinter as tk
from tkinter import Tk, Button, Checkbutton, Text, Label, filedialog, messagebox
from PIL import Image, ImageTk
from argparse import Namespace
from os.path import join, basename
from datetime import datetime
import numpy as np
import subprocess
from ctypes import c_uint, c_wchar_p

# class


class IDSCamera:
    def __init__(self, cameraParametersPath):
        # parameters
        self.width = 2456
        self.height = 2054
        self.bitspixel = 32  # for colormode = IS_CM_BGRA8_PACKED
        self.lineinc = self.width * int((self.bitspixel + 7) / 8)

        # init camera
        self.camera = ueye.HIDS(0)
        self.ret = ueye.is_InitCamera(self.camera, None)
        self.check(info='initial')
        '''
        # set BGRA8 color mode
        self.ret = ueye.is_SetColorMode(self.camera, ueye.IS_CM_BGRA8_PACKED)
        self.check(info='set color mode')

        # set region of interest
        rect_aoi = ueye.IS_RECT()
        rect_aoi.s32X = ueye.int(0)
        rect_aoi.s32Y = ueye.int(0)
        rect_aoi.s32Width = ueye.int(self.width)
        rect_aoi.s32Height = ueye.int(self.height)
        ueye.is_AOI(self.camera, ueye.IS_AOI_IMAGE_SET_AOI,
                    rect_aoi, ueye.sizeof(rect_aoi))
        self.check(info='set region of interest')
        '''
        # load parameter
        self.ret = ueye.is_ParameterSet(
            self.camera, ueye.IS_PARAMETERSET_CMD_LOAD_FILE, c_wchar_p(cameraParametersPath), c_uint(0))
        self.check(info='load parameter')

        # allocate memory
        self.mem_ptr = ueye.c_mem_p()
        mem_id = ueye.int()
        self.ret = ueye.is_AllocImageMem(
            self.camera, self.width, self.height, self.bitspixel, self.mem_ptr, mem_id)
        self.check(info='allocate memory')

        # set active memory region
        self.ret = ueye.is_SetImageMem(self.camera, self.mem_ptr, mem_id)
        self.check(info='set active memory region')

        # continuous capture to memory
        self.ret = ueye.is_CaptureVideo(self.camera, ueye.IS_DONT_WAIT)
        self.check(info='continuous capture to memory')

    def check(self, info):
        assert self.ret == 0, 'the camera does not successful {}, the return code {}.'.format(
            info, self.ret)

    def get_image(self):
        image = ueye.get_data(self.mem_ptr, self.width, self.height,
                              self.bitspixel, self.lineinc, copy=True)
        # because the cameraOptimalParameters uses BGRA mode to capture pictures and PIL API uses RGBA mode,
        # then needs to convert to RGBA mode, in addition,  the alpha channel has not any value.
        # So, I select the channel with RGB.
        image = np.reshape(image, (self.height, self.width, 4))[:, :, 2::-1]
        return image

    def release(self):
        self.ret = ueye.is_StopLiveVideo(self.camera, ueye.IS_FORCE_VIDEO_STOP)
        self.check(info='stop live video')
        self.ret = ueye.is_ExitCamera(self.camera)
        self.check(info='exit camera')


class GUI:
    def __init__(self, projectParams):
        self.camera = IDSCamera(
            cameraParametersPath=projectParams.cameraParametersPath)
        self.projectParams = projectParams
        self.folderPath = None

        # window
        self.window = Tk()
        self.window.geometry('{}x{}'.format(
            self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.window.title('IDS Camera GUI')

        # tkinter variable
        self.uploadBooleanVar = tk.BooleanVar()

        # button
        self.imageFolderPathButton = Button(
            self.window, text='影像存放位置', fg='black', bg='white', command=self.browse_folder)
        self.shootButton = Button(
            self.window, text='拍照', fg='black', bg='white', command=self.take_picture)

        # checkbutton
        self.uploadCheckbutton = Checkbutton(
            self.window, text='拍照並自動上傳', fg='black', variable=self.uploadBooleanVar, onvalue=True, offvalue=False)

        # label
        self.sampleNameLabel = Label(self.window, text='樣本名稱', fg='black')
        self.galleryTextLabel = Label(self.window, text='即時影像', fg='black')
        self.galleryImageLabel = Label(self.window, text='', fg='black')
        self.imagePathLabel = Label(self.window, text='', fg='black')

        # text
        self.sampleNameText = Text(self.window, height=2, width=10)

    def browse_folder(self):
        self.folderPath = filedialog.askdirectory(initialdir='./')

    def upload_image(self, filepath):
        subprocess.run(['scp', filepath, '{}@{}:{}'.format(self.projectParams.user,
                                                           self.projectParams.ip, join(self.projectParams.targetPath, basename(filepath)))])

    def take_picture(self):
        if self.folderPath is None:
            messagebox.showinfo(title='錯誤', message='尚未選取影像存放位置！')
        else:
            filename = join('{}_{}.png'.format(
                self.sampleNameText.get('1.0', 'end-1c'), datetime.now().strftime('%Y%m%d%H%M%S%f')))
            self.image.save(join(self.folderPath, filename))
            self.imagePathLabel.config(
                text='影像位置: {}'.format(join(self.folderPath, filename)))
            if self.uploadBooleanVar.get():
                self.upload_image(filepath=join(self.folderPath, filename))

    def get_realtime_image(self):
        # the self.camera.get_image() will return RGB image array
        self.image = Image.fromarray(self.camera.get_image(), mode='RGB')
        self.imageTk = ImageTk.PhotoImage(self.image.resize(
            self.projectParams.guiImageSize))  # resize the image
        self.galleryImageLabel.config(image=self.imageTk)
        self.galleryImageLabel.image = self.imageTk
        self.galleryImageLabel.after(1, self.get_realtime_image)

    def run(self):

        # position, 1st column
        self.imageFolderPathButton.pack(anchor=tk.NW)
        self.sampleNameLabel.pack(anchor=tk.NW)
        self.sampleNameText.pack(anchor=tk.NW)
        self.shootButton.pack(anchor=tk.NW)
        self.uploadCheckbutton.pack(anchor=tk.NW)

        # position, 2nd column
        self.galleryTextLabel.pack(anchor=tk.N)
        self.galleryImageLabel.pack(anchor=tk.N)
        self.imagePathLabel.pack(anchor=tk.N)

        # run
        self.get_realtime_image()
        self.window.mainloop()
        self.camera.release()


if __name__ == '__main__':
    # parameters
    projectParams = Namespace(**{'guiImageSize': [500, 500],
                                 'cameraParametersPath': 'cameraParameters.ini',
                                 'ip': '',
                                 'user': '',
                                 'targetPath': '~/Desktop/temp'})

    # GUI
    gui = GUI(projectParams=projectParams)
    gui.run()
