from os import walk
from PIL import Image

from app import *

# Helper Constant and Function to Delete the Old Xray
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def file_saver(filename):
    file = os.path.splitext(filename)
    org = Image.open(os.path.join(app.config['UPLOAD_FOLDER']+'tmp/', filename))
    org.save(os.path.join(app.config['UPLOAD_FOLDER']+'tmp/', (file[0] + '.png')))
    
    return str(file[0] + '.png')

def erase_dir():
    f = next(walk('static/uploads/tmp/'), (None, None, []))[2]
    for ele in f:
        os.remove('static/uploads/tmp/'+ele)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS