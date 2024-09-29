from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from werkzeug.utils import secure_filename
from encryption import encrypt_file, decrypt_file, generate_key

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Home page with upload form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle file uploads and encryption
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Generate AES key and encrypt the file
        key = generate_key()
        encrypted_file_path = encrypt_file(file_path, key)

        return f"File encrypted successfully. <a href='/download/{os.path.basename(encrypted_file_path)}'>Download Encrypted File</a>"

# Route to download encrypted file
@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(file_path, as_attachment=True)

# Route for decrypting an encrypted file
@app.route('/decrypt', methods=['POST'])
def decrypt():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    if file:
        # Assume the key is provided for this demo
        key = generate_key()

        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Decrypt the file
        decrypted_file_path = decrypt_file(file_path, key)

        return f"File decrypted successfully. <a href='/download/{os.path.basename(decrypted_file_path)}'>Download Decrypted File</a>"

# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)
