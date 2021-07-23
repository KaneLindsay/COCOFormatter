"""Creates training FITS for YOLO algorithm by parsing XLSX FITS files for the centre point of the object
and generating co-ordinates for a bounding box around them.
"""
import pandas as pd
import os
# Run script to convert FITS images to BMP output in 'images'
import fitstoimg

def xslx_reader(path: str):
    data = pd.read_excel(path)

    for i in range(len(data)):
        # Create path to save new data to
        file_name = data.iloc[i]['Filename (.fits)']
        file_name = file_name[1:-1]+".txt"
        # Path for writing data files
        save_path = "C:\\Users\\kanel\\PycharmProjects\\XSLX2YOLO\\YOLO\\data"
        complete_path = os.path.join(save_path, file_name)
        print(complete_path)

        # Read data from XSLX
        detection_class = "0"
        x = str(data.iloc[i]['Xpixel'])
        y = str(data.iloc[i]['Ypixel'])
        width = "50"
        height = "50"

        # Write data to new file
        f = open(complete_path, "w")
        f.write(detection_class + " " + x + " " + y + " " + width + " " + height)
        f.close()


XLSXpath = "satellite_data_13_12_18.xlsx"
xslx_reader(XLSXpath)




