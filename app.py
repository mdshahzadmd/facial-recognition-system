from flask import Flask, request, jsonify, render_template, send_from_directory
import os
from werkzeug.utils import secure_filename
import pickle
from model_utils import load_encodings, save_encodings, register_face, identify_faces


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWN_DIR = os.path.join(BASE_DIR, 'known_faces')
DATA_DIR = os.path.join(BASE_DIR, 'data')
ENCODINGS_PATH = os.path.join(DATA_DIR, 'encodings.pkl')
ALLOWED_EXT = {'png', 'jpg', 'jpeg'}


os.makedirs(KNOWN_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16MB


# Load or initialize encodings
encodings_db = load_encodings(ENCODINGS_PATH)


@app.route('/')
def index():
	return render_template('index.html')


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT


@app.route('/register', methods=['POST'])
def register():
	name = request.form.get('name', '').strip()
	file = request.files.get('photo')
	if not name:
		return jsonify({'success': False, 'error': 'Name is required'}), 400
	if not file or file.filename == '':
		return jsonify({'success': False, 'error': 'Photo is required'}), 400
	if not allowed_file(file.filename):
		return jsonify({'success': False, 'error': 'Invalid file type'}), 400

	filename = secure_filename(f"{name}_{file.filename}")
	save_path = os.path.join(KNOWN_DIR, filename)
	file.save(save_path)

	ok, msg = register_face(save_path, name, encodings_db)
	if not ok:
		return jsonify({'success': False, 'error': msg}), 400

	save_encodings(encodings_db, ENCODINGS_PATH)
	return jsonify({'success': True, 'message': 'Registered successfully'})


@app.route('/identify', methods=['POST'])
def identify():
	file = request.files.get('photo')
	if not file or file.filename == '':
		return jsonify({'success': False, 'error': 'Photo is required'}), 400
	if not allowed_file(file.filename):
		return jsonify({'success': False, 'error': 'Invalid file type'}), 400

	# Add your face identification logic here
	# Example: result = identify_faces(file, encodings_db)
	# return jsonify(result)


if __name__ == "__main__":
	app.run(debug=True)