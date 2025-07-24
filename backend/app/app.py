from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
import os
import pickle
import easyocr
from tensorflow.keras.preprocessing.sequence import pad_sequences

app = Flask(__name__)
CORS(app)

# ====== Load model ======
MODEL_PATH = os.path.abspath("rnn_model.h5")
model = tf.keras.models.load_model(MODEL_PATH)

# ====== Load tokenizer ======
TOKENIZER_PATH = os.path.abspath("tokenizer.pkl")
with open(TOKENIZER_PATH, 'rb') as f:
    tokenizer = pickle.load(f)

MAX_SEQUENCE_LENGTH = 100 

# ====== Init EasyOCR  ======
reader = easyocr.Reader(['id', 'en'])

# ====== Preprocess Text Function ======
def preprocess_text(text):
    sequence = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(sequence, maxlen=MAX_SEQUENCE_LENGTH, padding="post", truncating="post")
    return padded

# ====== Endpoint untuk teks langsung ======
@app.route('/api/detect-text', methods=['POST'])
def detect_text():
    data = request.get_json()
    text = data.get('text', '')

    if not text:
        return jsonify({'error': 'Text tidak boleh kosong'}), 400

    processed = preprocess_text(text)
    prediction = model.predict(processed)[0][0]

    result = {
        'status': 'Terdeteksi Iklan Judi' if prediction > 0.5 else 'Tidak Terindikasi Iklan Judi',
        'confidence': f'{prediction * 100:.2f}%',
        'raw_confidence': float(prediction)
    }

    return jsonify(result)

# ====== Endpoint untuk gambar dengan OCR ======
@app.route('/api/detect-image', methods=['POST'])
def detect_image():
    if 'image' not in request.files:
        return jsonify({'error': 'File gambar tidak ditemukan'}), 400

    image_file = request.files['image']
    image_bytes = image_file.read()

    # OCR menggunakan easyocr
    ocr_result = reader.readtext(image_bytes, detail=0)
    extracted_text = ' '.join(ocr_result)

    if not extracted_text.strip():
        return jsonify({'error': 'Teks tidak ditemukan di dalam gambar'}), 400

    # Prediksi
    processed = preprocess_text(extracted_text)
    prediction = model.predict(processed)[0][0]

    result = {
        'ocr_text': extracted_text,
        'status': 'Terdeteksi Iklan Judi' if prediction > 0.5 else 'Tidak Terindikasi Iklan Judi',
        'confidence': f'{prediction * 100:.2f}%',
        'raw_confidence': float(prediction)
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

