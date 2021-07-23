# Author : Dong Hyun Kim
import os
import numpy as np
from PIL import Image
from astropy.io import fits
import img_scale

dir_path = os.getcwd()
for filename in os.listdir(dir_path+"\\FITS"):
    if filename.endswith(".fits"):
        image_data = fits.getdata("FITS\\"+filename)
        if len(image_data.shape) == 2:
            sum_image = image_data
        else:
            sum_image = image_data[0] - image_data[0]
            for single_image_data in image_data:
                sum_image += single_image_data  

        sum_image = img_scale.sqrt(sum_image, scale_min=0, scale_max=np.amax(image_data))
        sum_image = sum_image * 200
        im = Image.fromarray(sum_image)
        if im.mode != 'RGB':
            im = im.convert('RGB')
    
        im.save(dir_path+"\\YOLO\\images\\"+filename+".bmp")
        im.close()

