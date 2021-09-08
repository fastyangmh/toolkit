# import
import os
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime

# global variables
UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
HTML_CONTENT = '''
<!doctype html>
<title>Upload image</title>
<center>
    <h1>Upload image</h1>
</center>
<style>
    input {
        padding: 5px 15px;
        background: #ccc;
        border: 0 none;
        cursor: pointer;
        -webkit-border-radius: 5px;
        border-radius: 5px;
        height: 50px;
        width: 200px;
    }
</style>
<form action="" method=post enctype=multipart/form-data>
    <center>
        <p>
            <input type="file" name="file" accept="image/*" capture="camera">
        </p>
        <p>
            <input type=submit value=Upload>
        </p>
    </center>
</form>
'''

# flask
app = Flask(__name__, template_folder='./')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# def


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = '{}.{}'.format(datetime.now().strftime(
                '%Y%m%d%H%M%S%f'), filename.rsplit('.', 1)[1])
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                   filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return HTML_CONTENT


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
