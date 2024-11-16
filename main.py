from flask import Flask,render_template, request, redirect, url_for, flash, abort, session, jsonify
import json
import os.path

app = Flask(__name__,template_folder="templates")
app.secret_key = 'kabra.anirudh'

@app.route("/activate")
def activate():
    return render_template('activate.html')

@app.route('/')
def home():
    print(session)
    return render_template('home.html', codes = session.keys())

@app.route('/your-url', methods = ['GET', 'POST'])
def your_url():
    
    if request.method == 'POST':

        urls = {}

        if os.path.exists('urls.json'):
            with open('urls.json') as url_file:
                urls = json.load(url_file)

        if request.form['code'] in urls.keys():
            flash("This short name is another taken, please use another name.")
            return redirect(url_for('home'))

        urls[request.form['code']] = {'url':request.form['url']}

        with open('urls.json', 'w') as url_file:
            json.dump(urls, url_file)
            session[request.form['code']] = True

        return redirect(url_for('home')) # return render_template('your_url.html', code = request.form['code'])
    
    else:
        return redirect(url_for('home'))
    
@app.route('/<string:code>')
def redirect_to_url(code):

    if os.path.exists('urls.json'):
        with open('urls.json') as url_file:
            urls = json.load(url_file)

    if code in urls.keys():
        if 'url' in urls[code].keys():
            return redirect(urls[code]['url'])
    return abort(404)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html')

@app.route('/api')
def api():
    return jsonify(list(session.keys()))




 