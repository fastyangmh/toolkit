import subprocess
import os

input_dir='/Users/yangmh/Desktop/data22000/'
output_dir='/Users/yangmh/Desktop/data16000/'

if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

for root,dirs,file in os.walk(input_dir):
    files=sorted(file)

for file in files:
    input_filepath=os.path.join(input_dir,file)
    output_filepath=os.path.join(output_dir,file)
    subprocess.run('sox {} -r 16k {}'.format(input_filepath,output_filepath),shell=1,check=1)