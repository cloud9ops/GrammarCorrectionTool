from flask import Flask, request, render_template, send_file
import os
from checker import process_docx_paragraphs
from werkzeug.utils import secure_filename
import io

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "❌ No file part", 400

        uploaded_file = request.files['file']

        if uploaded_file.filename == '':
            return "❌ No selected file", 400

        if uploaded_file and uploaded_file.filename.endswith('.docx'):
            filename = secure_filename(uploaded_file.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], f"corrected_{filename}")

            uploaded_file.save(input_path)
            process_docx_paragraphs(input_path, output_path)

            # Stream file to client then remove both files
            def cleanup_and_stream():
                with open(output_path, 'rb') as f:
                    data = f.read()
                os.remove(input_path)
                os.remove(output_path)
                return data

            return send_file(
                io.BytesIO(cleanup_and_stream()),
                download_name=f"corrected_{filename}",
                as_attachment=True
            )

        return "❌ Invalid file type. Only .docx allowed.", 400

    return render_template('index.html')


if __name__ == '__main__':
    # Makes the server available to other machines on the same network
    app.run(host='0.0.0.0', port=5000, debug=True)
