from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'secret1342'

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/HOTEL_EL_MALINCHE'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

# Inicializar SQLAlchemy
db = SQLAlchemy(app)

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
