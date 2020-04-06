"""
flask_mailroom project
created by philip korte
"""

import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor

app = Flask(__name__)
app.secret_key = b'\x9d\xb1u\x08%\xe0\xd0p\x9bEL\xf8JC\xa3\xf4J(hAh\xa4\xcdw\x12S*,u\xec\xb8\xb8'


@app.route('/')
def home():
    """ redirects to home page """
    return redirect(url_for('all'))


@app.route('/donations/')
def all():
    """ view all donation """
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)


@app.route('/create/', methods=['GET', 'POST'])
def create():
    """ add a new donation from an existing donor """
    if request.method == 'POST':
        try:
            donor = Donor.select()\
                         .where(Donor.name == request.form['name_donor'])\
                         .get()
        except Donor.DoesNotExist:
            return render_template('create.jinja2'\
                                   , error=f"{request.form['name_donor']} is not a current donor.")
        value = request.form['donation']

        Donation(donor=donor, value=value).save()

        return redirect(url_for('all'))

    return render_template('create.jinja2')


@app.route('/single/', methods=['GET', 'POST'])
def single():
    """ select a single donor to see their donations """
    if request.method == 'POST':
        try:
            donor = Donor.select()\
                         .where(Donor.name == request.form['name_donor'])\
                         .get()
        except Donor.DoesNotExist:
            return render_template('single.jinja2'\
                                   , error=f"{request.form['name_donor']} is not a current donor.")
        return redirect(url_for('one_donor', name=donor.name))

    return render_template('single.jinja2')


@app.route('/donations/<name>/')
def one_donor(name):
    """ show only a single donor's donations """
    donations = Donation.select(Donation, Donor)\
                        .join(Donor) \
                        .where(Donor.name == name)

    return render_template('donations.jinja2', donations=donations)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)
