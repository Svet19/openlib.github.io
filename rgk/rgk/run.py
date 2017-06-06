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
    # protect this func. to display user list.
    def __repr__(self):
        return '<User %r><Pass %r><Email %r><Org %r><First %r><Last %r>' % (self.uname, self.pword, self.email,
                                                                            self.org, self.fname, self.lname)

## ROUTE FOR THE DEFAULT URL
@app.route('/')
def main():
    return render_template('test.html')

## ROUTE FOR LOGIN CHECK
@app.route('/chkLogin', methods = ['POST'])
def chkLogin():
    if request.method == 'POST':
        # Get the appliance usage info
        if 'uname' in request.form:
            uchk = request.form['uname']
        if 'pword' in request.form:
            pchk = request.form['pword']
        if userDb.query.filter_by(uname=str(uchk),pword=str(pchk)).first():
            uid = userDb.query.filter_by(uname=str(uchk)).first()
            res = {'prc':'1','umsg':'Welcome, '+uid.fname+' '+uid.lname+'.','unm':uid.uname}     
            session['uname'] = uid.uname
        else:
            res = {'prc':'0'}
                                    
    return jsonify(stat = res)

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

## ROUTE FOR MODEL INSERT
@app.route('/createMod', methods = ['POST'])
def createMod():
    if request.method == 'POST':
        unm = request.form['recid']
        #uid = userDb.query.filter_by(uname=str(uchk)).first()
        res = usrData(unm)
        tblCreate = '<form class="form-horizontal" method="POST" id="tblForm" style="height: 500px;overflow-y: auto;">' \
                    '<div class="form-group row has-feedback">' \
                    '<div class="col-xs-12">' \
                    '<label for="txtMnm" class="control-label">Model Name:</label>' \
                    '<input class="form-control" id="txtMnm" type="text" placeholder="Enter model name" required>' \
                    '<span class="glyphicon form-control-feedback" aria-hidden="true"></span>' \
                    '</div>' \
                    '</div>' \
                    '<hr>' \
                    '<div class="form-group row has-feedback">' \
                    '<div class="col-xs-4">' \
                    '<label for="txtAuth" class="control-label">Name & Affiliation of Author:</label>' \
                    '<input class="form-control" id="txtAuth" type="text" placeholder="Enter name and affiliation" required>' \
                    '<label for="txtdop" class="control-label">Date of Publication:</label>' \
                    '<input class="form-control" id="txtdop" type="date" required>' \
                    '<label for="txtver" class="control-label">Version Information:</label>' \
                    '<input class="form-control" id="txtver" type="text" placeholder="Enter model version" required>' \
                    '<span class="glyphicon form-control-feedback" aria-hidden="true"></span>' \
                    '</div>' \
                    '<div class="col-xs-4">' \
                    '<label for="txtMsym" class="control-label">Model Symbol:</label>' \
                    '<textarea  class="form-control" rows="8" id="txtMsym" placeholder="Enter model symbol" required></textarea>' \
                    '<span class="glyphicon form-control-feedback" aria-hidden="true"></span>' \
                    '</div>' \
                    '<div class="col-xs-4">' \
                    '<label for="txtAcc" class="control-label">Accredition:</label> <br>' \
                    '<textarea  class="form-control" rows="8" id="txtAcc" placeholder="Enter accredition" required></textarea>' \
                    '<span class="glyphicon form-control-feedback" aria-hidden="true"></span>' \
                    '</div>' \
                    '</div>' \
                    '<hr>' \
                    '<div class="form-group row has-feedback">' \
                    '<div class="col-xs-6">' \
                    '<label for="txtma" class="control-label">Model Accessibility:</label>' \
                    '<textarea class="form-control" id="txtma" rows="3" placeholder="Enter model accessibility details" required></textarea>' \
                    '<label for="txtpd" class="control-label">Proprietary Documentation:</label>' \
                    '<textarea class="form-control" id="txtpd" rows="3" placeholder="Enter details" required></textarea>' \
                    '<span class="glyphicon form-control-feedback" aria-hidden="true"></span>' \
                    '</div>' \
                    '<div class="col-xs-6 col-md-6">' \
                    '<label for="txtcat" class="control-label">Type/Category of Model:</label>' \
                    '<textarea  class="form-control" rows="8" id="txtcat" placeholder="Enter model type" required></textarea>' \
                    '<span class="glyphicon form-control-feedback" aria-hidden="true"></span>' \
                    '</div>' \
                    '</div>' \
                    '<hr>' \
                    '<div class="form-group row has-feedback">' \
                    '<div class="col-xs-12 col-md-12">' \
                    '<label for="txtbtb" class="control-label">Brief Theoretical Background:</label>' \
                    '<textarea  class="form-control" rows="8" id="txtbtb" placeholder="Enter details" required></textarea>' \
                    '<span class="glyphicon form-control-feedback" aria-hidden="true"></span>' \
                    '</div>' \
                    '</div>' \
                    '<hr>' \
                    '<div class="form-group row has-feedback">' \
                    '<div class="col-xs-6 col-md-6">' \
                    '<label for="txtms" class="control-label">Model Specifications:</label>' \
                    '<textarea class="form-control" id="txtms" rows="4" placeholder="Enter model specifications" required></textarea>' \
                    '<span class="glyphicon form-control-feedback" aria-hidden="true"></span>' \
                    '</div>' \
                    '<div class="col-xs-6 col-md-6">' \
                    '<label for="txtdep" class="control-label">Model Dependencies:</label>' \
                    '<textarea  class="form-control" rows="4" id="txtdep" placeholder="Enter dependencies" required></textarea>' \
                    '<span class="glyphicon form-control-feedback" aria-hidden="true"></span>' \
                    '</div>' \
                    '</div>' \
                    '<hr>' \
                    '<div class="form-group row has-feedback">' \
                    '<div class="col-xs-12 col-md-12">' \
                    '<label for="txtinfo" class="control-label">Interfacing Information:</label>' \
                    '<textarea  class="form-control" rows="4" id="txtinfo" placeholder="Enter details" required></textarea>' \
                    '<span class="glyphicon form-control-feedback" aria-hidden="true"></span>' \
                    '</div>' \
                    '</div>' \
                    '<hr>' \
                    '<div class="form-group row">' \
                    '<div class="col-xs-6">' \
                    '<label for="txtpd" class="control-label">Diagramatic Representation:</label>' \
                    '<a href="#" class="btn btn-primary btn-block">Load Image</a>' \
                    '<img class="form-control" id="imgMod" rows="10"></img>' \
                    '</div>' \
                    '<div class="col-xs-6 col-md-6">' \
                    '<label for="txtint" class="control-label">Interfacing Capabilities for HIL Simulations:</label>' \
                    '<textarea  class="form-control" rows="4" id="txtint" placeholder="Enter details" required></textarea>' \
                    '<span class="glyphicon form-control-feedback" aria-hidden="true"></span>' \
                    '</div>' \
                    '</div>' \
                    '<hr>' \
                    '<div class="form-group row">' \
                    '<div class="col-xs-12 col-md-12">' \
                    '<a href="#" id="clickBtn" class="btn btn-primary btn-block">Add Model</a>' \
                    '</div>' \
                    '</div>' \
                    '</form>' 
    return jsonify(tblMenu=tblCreate)

## ROUTE FOR MODEL VALIDATION AND INSERT
@app.route('/subFrm', methods = ['POST'])
def subFrm():
    if request.method == 'POST':
        nm = request.form['txtMnm']
        print(request)
    return jsonify(resp=nm)

## GET THE USER DETAILS
def usrData(unm):
    uid = userDb.query.filter_by(uname=str(unm)).first()
    res = {'unm':uid.uname,'ufnm':uid.fname,
                  'ulnm':uid.lname,'uml':uid.email,'uorg':uid.org}     
    return res        
## RUN THE APP
if __name__ == '__main__':    

    db.create_all()    
    #print(userDb.query.all())
    #input('Press Enter to start the server')
    app.run( 
        #host="0.0.0.0",
        port=80,
        #debug=True
    )
