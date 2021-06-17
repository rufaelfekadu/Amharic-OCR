import os
import cv2
import ocr as oc
from flask import Flask, render_template, request, flash, url_for, send_from_directory
from werkzeug.utils import redirect, secure_filename

UPLOAD_FOLDER = r'/home/ruph/Documents/GitHub/OCR-nerd/flask_module/static/uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#
#
# @app.route('/', methods=['POST', 'Get'])
# def home():
#     if request.method == 'GET':
#         tasks = "hello"
#         return render_template("index.html", tasks=tasks)


@app.route('/about')
def about():
    return "welcome about"


@app.route('/', methods=['GET', 'POST'])
def upload_file():
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
            tasks = file.filename
            img = cv2.imread(dir)
            text = oc.ocr(img)

            return render_template('index.html', tasks='uploads/' + tasks, text=text)
            # return redirect(url_for('download_file', name=filename))
        
    tasks = "uploade images"
    return render_template('index.html', tasks=tasks)


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


if __name__ == '__main__':
    app.run(debug=True)
