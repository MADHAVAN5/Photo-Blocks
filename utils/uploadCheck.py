from os import walk
import cv2
import pandas as pd
import numpy as np
from PIL import Image

from app import *

# Helper Constant and Function to Delete the Old Xray
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def file_saver(filename):
    file = os.path.splitext(filename)
    org = Image.open(os.path.join(
        app.config['UPLOAD_FOLDER'], filename))
    org.save(os.path.join(app.config['UPLOAD_FOLDER'], (file[0] + '.png')))
    if file[1] != '.png':
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return str(file[0] + '.png')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS