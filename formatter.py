"""
Author: Kane Lindsay
Description: Creates COCO format training data from FITS images with XLSX descriptions.
How-To: Move all Liverpool Telescope FITS image files to 'FITS' folder with Excel file. Run this script.
        COCO JSON format annotations and BMP images are output in 'COCO' folder.
        This process can be repeated for as many times and new data will be added to the JSON.
        This can currently only be done with Liverpool Telescope data with file name starting with "h_e" due to scaling.
"""
import pandas as pd
import json
from datetime import datetime
import os
import numpy as np
from PIL import Image
from astropy.io import fits
import img_scale

DIRECTORY = os.getcwd()
DATETIME = datetime.today().strftime("%Y-%m-%dT%H:%M:%S+00:00")

# Convert FITS to BMP images
for filename in os.listdir(DIRECTORY + "\\FITS"):
    # If the file is a Liverpool Telescope FITS file
    if filename.startswith("h_e") and filename.endswith(".fits"):
        image_data = fits.getdata("FITS\\" + filename)
        if len(image_data.shape) == 2:
            sum_image = image_data
        else:
            sum_image = image_data[0] - image_data[0]
            for single_image_data in image_data:
                sum_image += single_image_data

        sum_image = img_scale.sqrt(sum_image, scale_min=0, scale_max=np.amax(image_data)) * 200
        im = Image.fromarray(sum_image)

        if im.mode != 'RGB':
            im = im.convert('RGB')

        # Resize image to a 2045 * 2056 square for training
        old_size = im.size
        new_size = (2056, 2056)
        new_im = Image.new("RGB", new_size)  # Default new image is already black which creates black border.
        new_im.paste(im, ((new_size[0] - old_size[0]) // 2,
                          (new_size[1] - old_size[1]) // 2))

        new_im.save(DIRECTORY + "\\COCO\\" + filename[:-5] + ".bmp")
        im.close()

# Create initial JSON string with no images or annotations
emptyCOCO = {
    "info": {
        "year": "2021",
        "version": "1",
        "description": "Space Object Dataset",
        "contributor": "Kane Lindsay",
        "url": "https://telescope.livjm.ac.uk/",
        "date_created": DATETIME
    },
    "licenses": [
        {
            "id": 1,
            "url": "",
            "name": "Unknown"
        }
    ],
    "categories": [
        {
            "supercategory": "object",
            "id": 1,
            "name": "object"
        },
    ],
    "images": [
    ],
    "annotations": [
    ]
}

# Create a new empty COCO JSON if one does not exist.
if not os.path.exists(DIRECTORY + "\\COCO\\data.json"):
    # Write JSON string to new JSON file
    s = json.dumps(emptyCOCO, indent=4)
    with open("COCO\\data.json", 'w') as f:
        f.write(s)


# Parse information from excel file to generate bounding boxes in COCO format
def xlsx_reader(path: str):
    excel_data = pd.read_excel(path)

    for i in range(len(excel_data)):
        # Get name of FITS image file
        filename = excel_data.iloc[i]['Filename (.fits)']
        filename = filename.replace("'", "")  # Remove inverted commas from image name

        if filename.startswith("h_e"):
            # Remove '.fits' file extension from file name
            filename = filename.replace(".fits", "")

            # Co-ordinates and bounding box dimensions
            x = excel_data.iloc[i]['Xpixel']
            y = excel_data.iloc[i]['Ypixel']
            width = 20
            height = 20

            # Read current information in JSON file
            d = open("COCO\\data.json", "r")
            json_data = json.loads(d.read())
            d.close()

            # Write image to dictionary
            json_data["images"].append({"id": len(json_data["images"])+1, "license": 1, "file_name": filename + ".bmp", "width": 2056,
                                        "height": 2056, "date_captured": excel_data.iloc[i]['Start Time (UTC)']})

            # Write annotation to dictionary
            json_data["annotations"].append({"id": len(json_data["annotations"])+1, "image_id": len(json_data["annotations"])+1, "category_id": 1,
                                             "bbox": [x - (width / 2), y - (height / 2), width, height],
                                             "area": width * height,
                                             "segmentation": [], "iscrowd": 0})

            # Write new entries to file
            d = open("COCO\\data.json", "w")
            d.write(json.dumps(json_data, indent=4))
            d.close()


file_found = False
filepath = ""
for filename in os.listdir(DIRECTORY + "\\FITS"):
    if filename.endswith(".xlsx"):
        if not file_found:
            file_found = True
            filepath = "FITS\\"+filename
        else:
            raise RuntimeError("Only one Excel file can be present at a time.")
xlsx_reader(filepath)
