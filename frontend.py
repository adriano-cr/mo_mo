from flask import Flask, render_template, redirect
from main import fai_le_cose
from classes.listing import Listing

app = Flask(__name__)

search_title = "seiko automatico"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/loading', methods=['GET'])
def loading():
    return render_template('loading.html')

@app.route('/launch_search', methods=['POST'])
def launch_search():
    le_cose = fai_le_cose(search_title)
    # return render_template('results.html', content = le_cose, search_title = search_title)
    return redirect('results.html', content = le_cose, search_title = search_title)

if __name__ == '__main__':
    app.run(debug=True)
