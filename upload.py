import os
import cv2
import testprint
from flask import Flask, flash, request, redirect, url_for, render_template, Response
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './static/uploads'
ALLOWED_EXTENSIONS = {'gif', 'webm', 'mp4', 'mov', 'avi'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    global cap
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            vid = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(vid)
            cap = cv2.VideoCapture(vid)
            return redirect(url_for('stream', file='show_vdo.html'))
            #return "Uploaded successfully"
            #return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload a video from Stanford Drone Dataset</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <button type="submit" class="btn btn-primary">Upload</button>
    </form>
    '''

#cap = cv2.VideoCapture(vid)

def generate_frames(cap):
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
        
        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
@app.route("/stream")
def stream():
    return render_template('show_vdo.html')


@app.route('/video')
def video():
    return Response(generate_frames(cap), mimetype='multipart/x-mixed-replace; boundary=frame')
            
@app.route("/stream2")
def stream2():
    output = testprint.result()
    return render_template('monitor.html', output=output)

@app.route('/violations')
def something(_argv):
    global vid1
    vid1 = "/home/soumyad/Videos/Screencast from 20-04-21 11:02:15 AM IST.webm"
    cap1 = cv2.VideoCapture(vid1)
    return Response(generate_frames(cap1), mimetype='multipart/x-mixed-replace; boundary=frame')

    
if __name__ == '__main__':
    app.run(debug = True, port=5005)