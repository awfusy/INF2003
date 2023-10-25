from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('home/index.html')

@app.route('/analysis.html')
def analysis():
    return render_template("home/analysis.html")

@app.route('/tables.html')
def tables():
    return render_template("home/tables.html")

if __name__ == "__main__":
    app.run(debug=True)