from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

import config
from hbar import HBar

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'photos')

hb = HBar(config.DB_NAME)

@app.route('/')
def index():
    term = request.args.get('q')
    products = hb.get_products(term)
    return render_template('index.html', products=products, term=term)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    photo_file = request.files.get('photo')
    photo_path = None
    if photo_file and photo_file.filename:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        filename = secure_filename(photo_file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        photo_file.save(path)
        photo_path = path
    in_test = bool(request.form.get('in_test'))
    hb.add_product(name, photo_path, in_test)
    return redirect(url_for('index'))

@app.route('/mark/<int:product_id>', methods=['POST'])
def mark(product_id):
    in_test = request.form.get('in_test') == '1'
    hb.mark_in_test(product_id, in_test)
    return redirect(url_for('index'))

@app.route('/rate/<int:product_id>', methods=['POST'])
def rate(product_id):
    score = int(request.form['score'])
    hb.add_rating(product_id, score)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
