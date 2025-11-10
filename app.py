from flask import Flask, render_template, request, redirect, url_for, session, flash, get_flashed_messages
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

# 🔹 Cargar las variables desde el archivo .env
load_dotenv()

#from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Configuración de la base de datos
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/HOTEL_EL_MALINCHE'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

# Inicializar SQLAlchemy
# db = SQLAlchemy(app)


# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = ('Hotel El Malinche', os.getenv("MAIL_USERNAME"))

mail = Mail(app)

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
    app.run(debug=True)
