from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
app.config["SECRET_KEY"] = "mi_clave_secreta"

class LoginForm(FlaskForm):
    username = StringField("Nombre de Usuario", validators=[DataRequired(), Length(min=3)])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField("Iniciar Sesión")

@app.route("/", methods=["GET"])
def index():
    return redirect(url_for("login"))  # Redirecciona correctamente a /login

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return f"Usuario: {form.username.data}"
    return render_template("index.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)
