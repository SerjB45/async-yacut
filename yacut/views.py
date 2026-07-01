from flask import render_template

from . import app, db


@app.route('/', methods=('GET',))
def short_link_view():
    return render_template('index.html')


@app.route('/files', methods=('GET',))
def upload_file_view():
    return render_template('upload_files.html')

