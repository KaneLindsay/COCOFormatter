# COCOFormatter

Generate YOLO data from FITS images + XLSX data sheet.

Program to convert FITS images to format accepted by Detectron2 COCO JSON format.

The input is recieved as a dump of FITS images and one Excel spreadsheet contraining the columns: Image filename, Name of the targeted object, NORAD ID, Observatory, Seconds of exposure, Exposure start time, and the pixel x and y and world RA DEC coordinates of the object.

Output is given as a set of BMP images of the same dimensions with a JSON file containing the class and label information.
