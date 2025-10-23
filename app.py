from flask import Flask, render_template, request, redirect, url_for, session, flash
#from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'secret1342'

# Configuración de la base de datos
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/HOTEL_EL_MALINCHE'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

# Inicializar SQLAlchemy
# db = SQLAlchemy(app)

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

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
