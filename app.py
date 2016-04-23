"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

import argparse
import os
from flask import Flask, render_template, request, redirect, url_for
from path_route import path_route
from path_microtrack import path_get_db, path_microtrack_add

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')

@app.route('/route')
def route_request():
    return path_route()

@app.route('/microtask/add')
def route_add_task():
    return path_microtrack_add()

@app.route('/microtask/get_db')
def route_get_db():
    return path_get_db()


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == "__main__":
    command_arguments = argparse.ArgumentParser(description="Viewer for geo A/B testing stand")
    command_arguments.add_argument('-port', default="55555", help='port to work on', type=int)
    command_arguments.add_argument('-path_to_static', default=None, help='path to static folder \
                                of working viewer, in this folder funnel images will be saved')
    command_arguments.add_argument('-production', default=False, action='store_true',
                                    help='run in gevent wsgi container')
    args = command_arguments.parse_args()

    if args.production is False:
        app.run(debug=True, host='0.0.0.0', port=args.port, passthrough_errors=True)
    else:
        from gevent.wsgi import WSGIServer
        http_server = WSGIServer(('', args.port), app)
        http_server.serve_forever()
