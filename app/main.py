from flask import Flask, request, jsonify, send_file
from uuid import uuid4
import os
from app.tasks import process_pdf
import logging

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    pdf_file = request.files['file']
    
    if pdf_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    unique_id = str(uuid4())
    folder_path = os.path.join(UPLOAD_FOLDER, unique_id)
    os.makedirs(folder_path, exist_ok=True)

    pdf_path = os.path.join(folder_path, pdf_file.filename)
    pdf_file.save(pdf_path)

    process_pdf.delay(pdf_path, folder_path)
    return jsonify({'unique_id': unique_id}), 200

@app.route('/status/<string:unique_id>', methods=['GET'])
def check_status(unique_id):
    folder_path = os.path.join(UPLOAD_FOLDER, unique_id)

    if not os.path.exists(folder_path):
        return jsonify({'error': 'Invalid unique ID'}), 404

    csv_path = os.path.join(folder_path, 'output.csv')
    if os.path.exists(csv_path):
        return send_file(csv_path, as_attachment=True)

    error_path = os.path.join(folder_path, 'error.txt')
    if os.path.exists(error_path):
        return send_file(error_path, as_attachment=True)

    return jsonify({'status': 'in-progress'}), 200

if __name__ == '__main__':
    app.run(debug=True)

