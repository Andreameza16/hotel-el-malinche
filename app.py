from flask import Flask, render_template, request, redirect, url_for, session, flash, get_flashed_messages, jsonify
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import requests


# Cargar las variables desde el archivo .env
load_dotenv()

app = Flask(__name__)
# Clave secreta
app.secret_key = os.getenv("SECRET_KEY")

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

# Inicializar SQLAlchemy
db = SQLAlchemy(app)

# PAYPAL
PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
PAYPAL_SECRET = os.getenv("PAYPAL_SECRET")
PAYPAL_API = "https://api-m.sandbox.paypal.com"

# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = ('Hotel El Malinche', os.getenv("MAIL_USERNAME"))

mail = Mail(app)
# MODELO TABLA
class Tipo_Habitacion(db.Model):
    __tablename__ = 'Tipo_Habitacion'
    Id_Tipo_Habitacion = db.Column(db.Integer, primary_key=True)
    Nombre_TipoHab = db.Column(db.String(100), nullable=False)
    Descripcion_Habitacion = db.Column(db.String(100))
    Precio_Habitacion = db.Column(db.Numeric(10, 2), nullable=False)


# --- RUTAS DE PAGO---
@app.route("/pago/<int:id>")
def pago(id):
    habitacion = Tipo_Habitacion.query.get(id)
    if not habitacion:
        return "Habitación no encontrada", 404
    return render_template("pago.html", habitacion=habitacion, paypal_client_id=PAYPAL_CLIENT_ID)


@app.route("/create-order", methods=["POST"])
def create_order():
    data = request.get_json()
    nombre = data.get("nombre")
    cedula = data.get("cedula")
    correo = data.get("correo")
    monto = data.get("monto")
    descripcion = data.get("descripcion")

    if not all([nombre, cedula, correo, monto, descripcion]):
        return jsonify({"error": "Faltan datos del cliente"}), 400

    # Obtener token de acceso PayPal
    auth_response = requests.post(
        f"{PAYPAL_API}/v1/oauth2/token",
        headers={"Accept": "application/json", "Accept-Language": "en_US"},
        data={"grant_type": "client_credentials"},
        auth=(PAYPAL_CLIENT_ID, PAYPAL_SECRET)
    )

    access_token = auth_response.json().get("access_token")
    if not access_token:
        return jsonify({"error": "No se pudo obtener token de PayPal"}), 500

    # Crear orden
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    payload = {
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {"currency_code": "USD", "value": str(monto)},
            "description": descripcion
        }]
    }

    r = requests.post(f"{PAYPAL_API}/v2/checkout/orders", headers=headers, json=payload)
    return jsonify(r.json())


@app.route("/capture-order", methods=["POST"])
def capture_order():
    data = request.get_json()
    order_id = data.get("orderID")
    nombre = data.get("nombre")
    cedula = data.get("cedula")
    correo = data.get("correo")

    # Obtener token de nuevo
    auth_response = requests.post(
        f"{PAYPAL_API}/v1/oauth2/token",
        headers={"Accept": "application/json", "Accept-Language": "en_US"},
        data={"grant_type": "client_credentials"},
        auth=(PAYPAL_CLIENT_ID, PAYPAL_SECRET)
    )

    access_token = auth_response.json().get("access_token")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    r = requests.post(f"{PAYPAL_API}/v2/checkout/orders/{order_id}/capture", headers=headers)
    result = r.json()

    if r.status_code in [200, 201]:
        # Enviar correo
        try:
            msg = Message(
                subject="Confirmación de Reserva - Hotel El Malinche 🌿",
                recipients=[correo],
                body=f"""
Estimado/a {nombre},

Tu pago ha sido completado exitosamente en Hotel El Malinche.

🧾 Detalles de la reserva:
- Cédula: {cedula}
- Habitación: {result['purchase_units'][0]['description']}
- Transacción: {result['id']}
- Estado: {result['status']}
- Monto: {result['purchase_units'][0]['amount']['value']} USD

Gracias por confiar en nosotros 🌿
Te esperamos pronto en Matagalpa.
"""
            )
            mail.send(msg)
            flash("Pago completado y correo enviado exitosamente ✅", "success")
        except Exception as e:
            print("Error enviando correo:", e)
            flash("Pago completado, pero ocurrió un error al enviar el correo.", "error")

        return jsonify({"status": "COMPLETED"})
    else:
        print("Error en respuesta PayPal:", result)
        flash("Error al procesar el pago.", "error")
        return jsonify({"status": "ERROR"}), 500



# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')

    if not email:
        flash("Por favor ingresa un correo válido.", "error")
        return redirect('/')

    try:
        msg = Message(
            subject="¡Gracias por suscribirte a Hotel El Malinche! 🌿",
            recipients=[email],
            body=(
                "Bienvenido a Hotel El Malinche.\n\n"
                "Gracias por suscribirte. Muy pronto recibirás nuestras promociones y descuentos exclusivos.\n\n"
                "— Equipo Hotel El Malinche"
            )
        )
        mail.send(msg)
        flash("¡Te has suscrito correctamente! Revisa tu correo.", "success")
    except Exception as e:
        print("ERROR:", e)
        flash("Hubo un problema al enviar el correo. Inténtalo nuevamente.", "error")
        print("MENSAJES GUARDADOS:", get_flashed_messages(with_categories=True))

    return redirect('/')

@app.route('/nosotros')
def nosotros():
    return render_template('sobrenosotros.html')

@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

# Habitaciones
@app.route('/habitaciones')
def habitaciones():
    return render_template('habitaciones.html')

@app.route('/habitaciones/suite')
def suite():
    return render_template('suite.html')

@app.route('/habitaciones/cabañas')
def cabaña():
    return render_template('cabañas.html')

@app.route('/habitaciones/familiar')
def familiar():
    return render_template('familiar.html')

@app.route('/habitaciones/individual')
def individual():
    return render_template('individual.html')

@app.route('/habitaciones/economica')
def economica():
    return render_template('economica.html')

@app.route('/habitaciones/villa')
def villa():
    return render_template('villa.html')

@app.route('/habitaciones/doble')
def doble():
    return render_template('doble.html')

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)