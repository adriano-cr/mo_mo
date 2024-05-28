from flask import Flask, render_template
import time

app = Flask(__name__)

@app.route('/')
def render_page(page, content):
    return render_template(page, content = "pagina di test")

# if __name__ == '__main__':
#     app.run(debug=True)
