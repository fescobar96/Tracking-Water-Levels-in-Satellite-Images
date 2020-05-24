import os
import json
import urllib
import h5py
import pickle as pk
import numpy as np
import server
from os.path import join
from os.path import dirname
from os.path import realpath
from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
from flask import send_from_directory
from flask import render_template
from flask import flash
from flask import Response
from werkzeug.utils import secure_filename
import base64

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/uploads/') 
ALLOWED_EXTENSIONS = set(['png', 'PNG', 'jpg', 'JPG', 'jpeg', 'JPEG'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 # max upload - 10MB
app.secret_key = 'secret'

# check if an extension is valid and that uploads the file and redirects the user to the URL for the uploaded file
def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def home():
	return render_template('index.html', result=None)

@app.route('/<a>')
def available(a):
	flash('{} coming soon!'.format(a))
	return render_template('index.html', result=None, scroll='second')

@app.route('/segmentation')
def assess():
	return render_template('index.html', result=None, scroll='second')


@app.route('/segmentation', methods=['GET', 'POST'])
def upload_and_classify():
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(url_for('assess'))
		
		file = request.files['file']

		if file.filename == '':
			flash('No selected file')
			return redirect(url_for('assess'))

		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename) # used to secure a filename before storing it directly on the filesystem
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

			filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			results = server.workflow(filepath)

			return render_template('results.html', results=results, scroll='second', filename=filename)
	
	flash('Invalid file format - please try your upload again.')
	return redirect(url_for('assess'))


@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'],
							   filename)

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080, debug=False)