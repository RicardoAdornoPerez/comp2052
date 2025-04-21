from flask import Flask, render_template, redirect, flash
from forms import RegistroForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "clave_segura_123"

@app.route("/registro", methods=["GET", "POST"])
def registro():
    form = RegistroForm()
    if form.validate_on_submit():
        flash("Usuario registrado correctamente.", "success")
        return redirect("/registro")
    return render_template("register.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)
