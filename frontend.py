from flask import Flask, render_template, redirect
from main import fai_le_cose
from classes.listing import Listing

app = Flask(__name__)

search_title = "seiko automatico"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/trigger_function', methods=['POST'])
def trigger_function():
    launch_search()
    return render_template('loading.html')

def launch_search():
    le_cose = fai_le_cose(search_title)
    # return render_template('index.html', title=le_cose.title, description=le_cose.description, img_url=le_cose.img)
    return render_template('results.html', content = le_cose, search_title = search_title)

if __name__ == '__main__':
    app.run(debug=True)
