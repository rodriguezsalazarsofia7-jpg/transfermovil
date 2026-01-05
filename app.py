from flask import Flask, request, jsonify
import smtplib
from email.message import EmailMessage
from datetime import datetime

app = Flask(__name__)

# === CONFIGURACIÓN DE CORREO ===
EMAIL_DESTINO = "rodriguezsalazarsofia7@gmail.com"
EMAIL_ORIGEN = "TU_CORREO_GMAIL@gmail.com"
EMAIL_PASSWORD = "CONTRASEÑA_DE_APLICACION"

def enviar_email(usuario, ip):
    msg = EmailMessage()
    msg["Subject"] = "Login detectado - TransferMovil"
    msg["From"] = EMAIL_ORIGEN
    msg["To"] = EMAIL_DESTINO

    msg.set_content(f"""
Inicio de sesión detectado

Usuario: {usuario}
Fecha: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
IP: {ip}

(No se envían contraseñas)
""")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ORIGEN, EMAIL_PASSWORD)
        server.send_message(msg)

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    usuario = data.get("usuario")
    password = data.get("password")

    # AUTENTICACIÓN DEMO
    if usuario == "admin" and password == "1234":
        enviar_email(usuario, request.remote_addr)
        return jsonify({"status": "ok"})
    else:
        return jsonify({"status": "error"}), 401

if __name__ == "__main__":
    app.run(debug=True)
