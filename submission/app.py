from flask import Flask, render_template, redirect, request, flash, session, url_for
from werkzeug.utils import secure_filename
from main_pointillism import pointillism
import os
import logging
import base64

connection = None
classObj = None

UPLOAD_FOLDER = './images/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET","POST"])
def home():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_name = os.path.join(app.config['UPLOAD_FOLDER'], filename) 
            file.save(file_name)
            pointillism(file_name)
            img = open(file_name, 'rb').read()
            img = str(base64.b64encode(img).decode("utf-8")) 
            os.remove(file_name)   
            return render_template('index.html',picture = img)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0",port="5013")