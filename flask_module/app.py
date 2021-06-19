import os
import cv2
import pytesseract

import ocr as oc
from flask import Flask, render_template, request, flash, url_for, send_from_directory
from werkzeug.utils import redirect, secure_filename

curdir = os.getcwd()
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#
#
@app.route('/', methods=['Get'])
def home():
    if request.method == 'GET':
        return render_template("index.html")


@app.route('/about')
def about():
    return "welcome about"


@app.route('/', methods=['POST'])
def upload_file():
    scanned_image = False
    lang = "amh"
    down = request.form.get('download')
    if down:
            return redirect(url_for('download_file', name=down))
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            # flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            # flash('No selected file')
            print("images not  saved")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = file.filename
            print(app.config['UPLOAD_FOLDER'])
            dir = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(dir)
            scanned_image = request.form.get('scanned-image')
            camera_image = request.form.get('camera-image')
            amh = request.form.get('select-amh')
            eng = request.form.get('select-eng')
            if scanned_image:
                scanned_image = True
            if amh:
                lang = 'amh'
            elif eng:
                lang = 'eng'
            elif amh and eng:
                lang = 'amh+eng'
            tasks = file.filename
            img = cv2.imread(dir)
            text, dir = oc.ocr(img, scanned_image, lang)
            # print(text)
            return render_template('index.html', tasks='uploads/' + tasks, text=text, dir=dir)
        
        

    return render_template('index.html')


curdir = os.path.join(os.path.pardir, 'output/')


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(curdir, name)


if __name__ == '__main__':
    app.run(debug=True)
