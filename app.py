from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import edge_tts
import asyncio
import os
import uuid

# 1. Inisialisasi Aplikasi Flask
app = Flask(__name__)

# 2. Atur CORS (Izinkan domain tertentu untuk mengakses API ini)
CORS(app, resources={r"/api/*": {"origins": ["https://kbbi.co.id", "https://www.kbbi.co.id"]}})

# Fungsi asinkron untuk memproses Text-to-Speech
async def generate_audio(text, voice, output_path):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

# 3. Buat Endpoint (Rute) untuk memproses permintaan dari Frontend
@app.route('/api/tts', methods=['POST'])
def tts_api():
    # Ambil data JSON yang dikirim dari Frontend
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({"error": "Teks tidak boleh kosong"}), 400

    text = data['text']
    # Gunakan suara default bahasa Indonesia (Gadis untuk wanita, Ardi untuk pria)
    voice = data.get('voice', 'id-ID-GadisNeural') 

    # Buat nama file audio unik agar tidak bentrok jika ada banyak permintaan bersamaan
    filename = f"audio_{uuid.uuid4().hex}.mp3"
    
    # Simpan di folder sementara (Render menggunakan sistem operasi Linux)
    filepath = os.path.join("/tmp", filename) if os.name != 'nt' else filename

    try:
        # Jalankan proses pembuatan audio
        asyncio.run(generate_audio(text, voice, filepath))
        
        # Kirim file audio yang sudah jadi kembali ke Frontend
        return send_file(filepath, mimetype="audio/mpeg", as_attachment=False)
        
    except Exception as e:
        return jsonify({"error": f"Terjadi kesalahan saat memproses audio: {str(e)}"}), 500

# Baris ini hanya digunakan jika Anda mengujinya secara lokal di komputer
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
