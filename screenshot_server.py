#! /bin/python3
from flask import Flask, send_file
import pyautogui
import io

app = Flask(__name__)

@app.route('/screenshot')
def screenshot():
    try:
        # Cattura lo screenshot
        img = pyautogui.screenshot()
        
        # Salva l'immagine in un buffer di memoria
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        
        # Restituisce l'immagine come risposta
        return send_file(buf, mimetype='image/png')
    except Exception as e:
        # Stampa l'errore nel log del server
        print(f"Errore: {e}")
        return "Errore interno del server", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)