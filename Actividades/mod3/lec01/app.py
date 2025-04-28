from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'clave_secreta'  # Necesaria para manejar sesiones de usuario

# Usuarios registrados (usuario: contraseña y rol)
usuarios = {
    'admin': {'password': 'admin2', 'rol': 'Administrador'},
    'saul': {'password': 'saul123', 'rol': 'Usuario'},
    'janiel': {'password': 'ronaldo123', 'rol': 'Editor'}
}

# Ruta principal (Dashboard)
@app.route('/')
def dashboard():
    if 'usuario' in session:
        return render_template('index.html', usuario=session['usuario'], rol=session['rol'])
    return redirect(url_for('login'))

# Ruta de Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = usuarios.get(username)
        
        if user and user['password'] == password:
            session['usuario'] = username
            session['rol'] = user['rol']
            return redirect(url_for('dashboard'))
        else:
            flash('Credenciales incorrectas', 'error')

    return render_template('login.html')

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
