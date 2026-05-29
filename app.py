from flask_cors import CORS

# Hanya izinkan website kbbi.co.id yang bisa memakai API Anda
CORS(app, resources={r"/api/*": {"origins": ["https://kbbi.co.id", "https://www.kbbi.co.id"]}})
