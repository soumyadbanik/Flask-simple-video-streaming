import cv2
import os
from flask import Flask, flash, request, redirect, url_for, render_template

UPLOAD_FOLDER = './static/uploads'
ALLOWED_EXTENSIONS = {'webm'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "super secret key"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No file selected')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template("index1.html") 
            
@app.route('/video', methods=['GET', 'POST'])
def show_vdo():
    return render_template("show_vdo.html")
        

if __name__ == '__main__':
    app.run(debug = True, port=5001)