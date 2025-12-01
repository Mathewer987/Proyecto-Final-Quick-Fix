from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def muro():
    return render_template("TrabajosPendientes.html")  # <-- acá ponés el nombre exacto del HTML

if __name__ == "__main__":
    app.run(debug=True)
