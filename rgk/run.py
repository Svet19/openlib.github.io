# -*- coding: utf-8 -*-
## IMPORT LIBRARIES
import uuid, os, glob, json, collections
from flask import Flask, Response, request, session, flash, url_for, redirect, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

## INITIALIZE THE FLASK APPLICATION
app = Flask(__name__)
app.secret_key = os.urandom(24)

## INITIALIZE THE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///survey.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

## DATABASE QUERY COMMANDS
'''
To add data to the userDb Table:
    user = userDb('inlusr','inlpass')
    db.session.add(user)
    db.session.commit()
    
To fetch data from the userDb:
    userDb.query.all()
    userDb.query.filter_by(pword='inlusr')
'''

## USER TABLE
class userDb(db.Model):
    id = db.Column('uid', db.Integer, primary_key=True)
    uname = db.Column(db.String(10), unique=True)
    pword = db.Column(db.String(10))
    email = db.Column(db.String(80))
    org = db.Column(db.String(10))
    fname = db.Column(db.String(10))
    lname = db.Column(db.String(10))

    def __init__(self, uname, pword, email, org, fname, lname):
        self.uname = uname
        self.pword = pword
        self.email = email
        self.org = org
        self.fname = fname
        self.lname = lname

    def __repr__(self):
        return '<User %r><Pass %r><Email %r><Org %r><First %r><Last %r>' % (self.uname, self.pword, self.email,
                                                                            self.org, self.fname, self.lname)

## ROUTE FOR THE DEFAULT URL
@app.route('/')
def main():
    return render_template('index.html')

## ROUTE FOR LOGIN CHECK
@app.route('/chkLogin', methods = ['GET', 'POST'])
def chkLogin():
    if request.method == 'POST':
        # Get the appliance usage info
        if 'uname' in request.form:
            uchk = request.form['uname']
        if 'pword' in request.form:
            pchk = request.form['pword']
        if userDb.query.filter_by(uname=str(uchk),pword=str(pchk)).first():
            msg = '1'
            session['uname'] = uchk
        else:
            msg = '0'
                                         
    return jsonify(stat = msg)

## ROUTE FOR CONTROL PANEL
@app.route('/cpanel')
def cpanel():

    # Get the user list
    uDet = userDb.query.with_entities(userDb.uname)
    uList = [uDet.uname for uDet in uDet.all()]
    uDet = userDb.query.with_entities(userDb.email)
    uMail = [uDet.email for uDet in uDet.all()]
    uDet = {'list':uList,'mail':uMail}
    uDet = zip(uDet['list'], uDet['mail'])
    return render_template('test.html', u = uDet)

## RUN THE APP
if __name__ == '__main__':    

    db.create_all()    

    app.run( 
        #host="0.0.0.0",
        port=80,
        #debug=True
    )
