from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Pass your Google Maps API key here
    return render_template("index.html", )

if __name__ == "__main__":
    app.run(debug=True)



