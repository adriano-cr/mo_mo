from flask import Flask, render_template
from main import fai_le_cose
import time

app = Flask(__name__)

@app.route('/')
def home():
    le_cose = fai_le_cose()
    return render_template('index.html', content = le_cose)

if __name__ == '__main__':
    app.run(debug=True)
