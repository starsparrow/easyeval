#! /usr/bin/env python

from flask import Flask, request, redirect, url_for, abort, render_template
import sqlalchemy
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    SECRET_KEY='developmentkey'
))
app.config.from_envvar('EASYEVAL_SETTINGS', silent=True)

from easyeval import easyeval

BASE_CAS_URL = 'https://cas.iu.edu/cas'
SESSION = {'username': ''}


def is_logged_in():
    return True if len(SESSION['username']) > 0 else False

def get_evals(author, recipient, evaltype):
    # Look stuff up in database and return it!
    pass
    

# URL ROUTING
@app.route('/')
def main():
    return render_template(
        'main.html',
        logged_in=is_logged_in(),
        name=SESSION['username']
    )


@app.route('/login')
def login():
    if not is_logged_in():
        if request.args.get('ticket') is None:
            return redirect(
                '{}/login?service={}'.format(BASE_CAS_URL, request.base_url)
            )
        else:
            r = requests.get(
                '{}/serviceValidate?service={}&ticket={}'.format(
                    BASE_CAS_URL,
                    request.base_url,
                    request.args.get('ticket'))
            )
            SESSION['username'] = ET.fromstring(r.text)[0][0].text
            return redirect(request.url_root)
    else:
        return redirect(request.url_root)


@app.route('/create')
def create_new_eval():
    return render_template(
        'create.html',
        logged_in=is_logged_in(),
        name=SESSION['username']
    )
    

@app.route('/doeval')
def do_eval():
   return 'I am not implemented yet!' 


@app.route('/evalsbyme')
def see_evals_by_me():
    return 'I am not implemented yet!'
    

@app.route('/evalsonme')
def see_evals_on_me():
    return 'I am not implemented yet!'

