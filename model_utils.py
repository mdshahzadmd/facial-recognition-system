import face_recognition
import os
import pickle
import numpy as np


# Encodings DB format:
# { 'names': [name1, name2, ...], 'encodings': [array1, array2, ...] }


def load_encodings(path):
	if os.path.exists(path):
		with open(path, 'rb') as f:
			return pickle.load(f)
	return {'names': [], 'encodings': []}




def save_encodings(db, path):
	with open(path, 'wb') as f:
		pickle.dump(db, f)




def register_face(image_path, name, db):
	"""Load image, detect face encodings and add them to db. Returns (ok, message)"""

	image = face_recognition.load_image_file(image_path)
	encs = face_recognition.face_encodings(image)
	if not encs:
		return False, 'No face found in the image.'
	# We'll take the first face found in the registration image
	encoding = encs[0]
	db['names'].append(name)
	db['encodings'].append(encoding)
	return True, 'Added'




def identify_faces(image_path, db, tolerance=0.45):
	image = face_recognition.load_image_file(image_path)
	face_locations = face_recognition.face_locations(image)
	face_encodings = face_recognition.face_encodings(image, face_locations)

	results = []
	for loc, enc in zip(face_locations, face_encodings):
		if not db['encodings']:
			results.append({'name': 'Unknown', 'location': loc, 'distance': None})
			continue
		distances = face_recognition.face_distance(db['encodings'], enc)
		best_idx = np.argmin(distances)
		best_dist = float(distances[best_idx])
		name = db['names'][best_idx] if best_dist <= tolerance else 'Unknown'
		results.append({'name': name, 'location': loc, 'distance': best_dist})
	return results