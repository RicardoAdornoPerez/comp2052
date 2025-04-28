from flask import Flask, request, redirect, url_for, session, render_template
from flask_principal import Principal, Permission, RoleNeed, Identity, identity_changed, identity_loaded, AnonymousIdentity

app = Flask(__name__)
app.secret_key = 'secreto123'  # Clave para manejar sesiones de usuario

# Inicializar el gestor de permisos
Principal(app)

# Definición de permisos basados en roles
admin_permission = Permission(RoleNeed('admin'))
editor_permission = Permission(RoleNeed('editor'))
user_permission = Permission(RoleNeed('user'))

# Simulación de usuarios en memoria (usuario: rol)
usuarios = {
    "admin": "admin",
    "editor": "editor",
    "usuario": "user"
}

# Página de inicio
@app.route('/')
def index():
    return render_template('index.html')

# Ruta de login
@app.route('/login/<username>')
def login(username):
    if username in usuarios:
        session['user'] = username
        identity_changed.send(app, identity=Identity(username))
        return f'Logueado como {username} (rol: {usuarios[username]})'
    return 'Usuario no encontrado', 404

# Ruta de logout
@app.route('/logout')
def logout():
    session.clear()
    identity_changed.send(app, identity=AnonymousIdentity())
    return redirect(url_for('index'))

# Área protegida para administradores
@app.route('/admin')
@admin_permission.require(http_exception=403)
def admin_area():
    return 'Área de Administración: Solo para administradores.'

# Área protegida para editores
@app.route('/editor')
@editor_permission.require(http_exception=403)
def editor_area():
    return 'Área de Edición: Solo para editores.'

# Área protegida para usuarios normales
@app.route('/user')
@user_permission.require(http_exception=403)
def user_area():
    return 'Área de Usuario: Solo para usuarios registrados.'

# Cargar identidad del usuario logueado
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    username = identity.id
    if username and username in usuarios:
        role = usuarios[username]
        identity.provides.add(RoleNeed(role))

# Página de error 403 (Acceso denegado)
@app.errorhandler(403)
def acceso_denegado(e):
    return 'Acceso denegado: No tienes permisos para entrar aquí.', 403

if __name__ == '__main__':
    app.run(debug=True)
