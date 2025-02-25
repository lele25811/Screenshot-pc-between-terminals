#! /bin/python3

#!/usr/bin/env python3
from flask import Flask, send_file
import pyautogui
import io
import subprocess
import time
import requests

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

def start_ngrok():
    """
    Avvia ngrok e restituisce l'URL pubblico.
    """
    # Avvia ngrok in una sottoprocesso
    ngrok_process = subprocess.Popen(['ngrok', 'http', '5000'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Aspetta qualche secondo per permettere a ngrok di avviarsi
    time.sleep(10)
    
    # Ottieni l'URL pubblico generato da ngrok
    try:
        ngrok_url = requests.get('http://localhost:4040/api/tunnels').json()['tunnels'][0]['public_url']
        print(f"Ngrok URL: {ngrok_url}")
    except Exception as e:
        print(f"Errore durante il recupero dell'URL di ngrok: {e}")
        ngrok_process.terminate()  # Termina ngrok in caso di errore
        ngrok_url = None
    
    return ngrok_process, ngrok_url

if __name__ == '__main__':
    # Avvia ngrok
    ngrok_process, ngrok_url = start_ngrok()
    
    if ngrok_url:
        print(f"Il server è accessibile all'URL: {ngrok_url}")
    else:
        print("Impossibile avviare ngrok. Verifica la configurazione.")
    
    # Avvia il server Flask
    app.run(host='0.0.0.0', port=5000)
    
    # Termina ngrok quando il server Flask si ferma
    ngrok_process.terminate()
