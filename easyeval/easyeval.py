#! /usr/bin/env python

from flask import Flask, request, session, redirect, url_for, render_template
import sqlalchemy
import requests
import xml.etree.ElementTree as ET
import json

app = Flask(__name__)
app.secret_key = 'a/a3iasdfl8af38aweijfzuighaiusreha'

from easyeval import easyeval

BASE_CAS_URL = 'https://cas.iu.edu/cas'

def is_logged_in():
    return True if 'username' in session else False

def get_evals(author, recipient, evaltype):
    '''Look stuff up in database and return it!'''
    pass


def list_forms():
    '''Get a list of forms from the JSON'''
    with app.open_resource('forms.json') as f:
        data = json.load(f)
        return [formid['title'] for formid in data[0]]


# URL ROUTING
@app.route('/')
def main():
    return render_template(
        'main.html',
        logged_in=is_logged_in(),
        name=session['username'] if 'username' in session else 'Guest'
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
            session['username'] = ET.fromstring(r.text)[0][0].text
            return redirect(request.url_root)
    else:
        return redirect(request.url_root)


@app.route('/logout')
def logout():
    if is_logged_in():
        session.pop('username', None)
        return redirect(request.url_root)


@app.route('/preview')
def list_forms_to_preview():
    return render_template('formstopreview.html', forms=list_forms())


@app.route('/preview/<form>')
def preview_eval(form):
    return 'I am not implemented yet!'
        


@app.route('/create')
def create_new_eval():
    return render_template(
        'create.html',
        logged_in=is_logged_in(),
        name=session['username'] if 'username' in session else 'Guest'
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

