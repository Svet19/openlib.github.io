# -*- coding: utf-8 -*-
import uuid, os, glob, json, collections
import pandas as pd
from flask import Flask, Response, request, session, flash, url_for, redirect, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from lib import *
from lib_analzye import *

##############################################################################
# DEFINE VARIABLES
##############################################################################

# Define the Utility rate ( in $/kWh)
u_rate = 0.5

# Appliance code:
#  dish: Dishwasher
#  laun: Dryer
#  acsu: Heating (S) |   Space Heater in Summer
#  acwi: Heating (W) |   Space Heater in Winter
#  ahsu: Cooling (S) |   Air Conditioner in Summer
#  ahwi: Cooling (W) |   Air Conditioner in Winter
#  wcsu: Shower (S)  |   Water Heater in Summer
#  wcwi: Shower (W)  |   Water Heater in Winter

# Define the appliance rating ( in watts)
app_power = {'dish':'300','laun':'5500','acsu':'1500','acwi':'1500',
             'ahsu':'2637','ahwi':'2637','wcsu':'5500','wcwi':'5500'}

# Define the appliance usage ( in hours/day)
app_usage = {'dish':'0.75','laun':'0.503','acsu':'2.579','acwi':'2.579',
             'ahsu':'8','ahwi':'8','wcsu':'0.86','wcwi':'0.86'}
app_def = {'power':app_power,'usage':app_usage}
a = ['dish','laun','acsu','acwi','ahsu','ahwi','wcsu','wcwi']
a_nm = ['Dishwasher','Dryer','Heating(S)','Heating(W)',
        'Cooling(S)','Cooling(W)','Shower(S)','Shower(W)']
c_nm = ['Comfort','Cost','Carbon']
##############################################################################
# DEFINE COST AND CARBON FUNCTIONS
##############################################################################

# Calculate the montly appliance usage cost and carbon footprint
def appCost(apptype,times_per_month,u_rate,app_def):
    # power in watts
    # u_rate in $/kWh
    #print(apptype,times_per_month,app_def['power'][apptype],u_rate)
    C = (float(app_def['power'][apptype])/1000)*float(times_per_month)*float(app_def['usage'][apptype])*float(u_rate)
    return C

def appCrbn(apptype,times_per_month,app_def):
    # power in watts
    C = (float(app_def['power'][apptype])/1000)*float(times_per_month)*float(app_def['usage'][apptype])*1.327
    return C

# Translate the carbon/cost values to AHP weights
def C_to_AHP(val):
    old_min = min(val)
    old_max = max(val)
    new_min = 1
    new_max = 5

    return [5 if int(round((((val[i] - old_min) * new_max) / old_max) + new_min, 3)) > 4.99
             else int(round((((val[i] - old_min) * new_max) / old_max) + new_min, 3)) for i in range(len(val))]

##############################################################################
# INITIALIZE THE FLASK APPLICATION
##############################################################################
app = Flask(__name__)

# Generate a secret random key for the session
app.secret_key = os.urandom(24)

##############################################################################
# INITIALIZE THE DATABASE
##############################################################################
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///survey.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class surveyAHP(db.Model):
    
    id = db.Column('survey_id', db.Integer, primary_key = True)
    wid = db.Column(db.String(6))
    # For criteria
    sl_comf = db.Column(db.Float)
    sl_cost = db.Column(db.Float)
    sl_carb = db.Column(db.Float)
    # For Alternatives
    sl_dish = db.Column(db.Float)
    sl_dry = db.Column(db.Float)
    sl_heatS = db.Column(db.Float)
    sl_heatW = db.Column(db.Float)
    sl_coolS = db.Column(db.Float)
    sl_coolW = db.Column(db.Float)
    sl_showS = db.Column(db.Float)
    sl_showW = db.Column(db.Float)
    # Appliance
    dsh_use = db.Column(db.String(6))
    run_dish = db.Column(db.String(6))
    dr_use = db.Column(db.String(6))
    run_dr = db.Column(db.String(6))
    sh_use = db.Column(db.String(6))
    run_heatS = db.Column(db.String(6))
    run_heatW = db.Column(db.String(6))
    ac_use = db.Column(db.String(6))
    run_coolS = db.Column(db.String(6))
    run_coolW = db.Column(db.String(6))
    wh_use = db.Column(db.String(6))
    run_showS = db.Column(db.String(6))
    run_showW = db.Column(db.String(6))
    wm_use = db.Column(db.String(6))
    # length vs. temp
    # heating at home
    coollen = db.Column(db.String(10))
    # cooling at home
    heatlen = db.Column(db.String(10))
    # shower at home
    showlen = db.Column(db.String(10))
    # demograph questions
    age = db.Column(db.String(10))
    zipCode = db.Column(db.String(10))
    gender = db.Column(db.String(10))

    def __init__(self, wid, sl_comf, sl_cost, sl_carb, sl_dish, sl_dry, sl_heatS, sl_heatW, sl_coolS, sl_coolW, sl_showS, sl_showW,
                 dsh_use, run_dish, dr_use, run_dr, sh_use, run_heatS, run_heatW, ac_use, run_coolS, run_coolW, wh_use,
                 run_showS, run_showW, wm_use, coollen, heatlen, showlen, age, zipCode, gender):
        
        self.wid = wid
        self.sl_comf = sl_comf
        self.sl_cost = sl_cost
        self.sl_carb = sl_carb
        self.sl_dish = sl_dish
        self.sl_dry = sl_dry
        self.sl_heatS = sl_heatS
        self.sl_heatW = sl_heatW
        self.sl_coolS = sl_coolS
        self.sl_coolW = sl_coolW
        self.sl_showS = sl_showS
        self.sl_showW = sl_showW
        self.dsh_use = dsh_use
        self.run_dish = run_dish
        self.dr_use = dr_use
        self.run_dr = run_dr
        self.sh_use = sh_use
        self.run_heatS = run_heatS
        self.run_heatW = run_heatW
        self.ac_use = ac_use
        self.run_coolS = run_coolS
        self.run_coolW = run_coolW
        self.wh_use = wh_use
        self.run_showS = run_showS
        self.run_showW = run_showW
        self.wm_use = wm_use
        self.coollen = coollen
        self.heatlen = heatlen
        self.showlen = showlen
        self.age = age
        self.zipCode = zipCode
        self.gender = gender

class resAHP(db.Model):
    
    id = db.Column('res_id', db.Integer, primary_key = True)
    rwid = db.Column(db.String(6))
    zipCode = db.Column(db.String(10))
    # For criteria
    r_comf = db.Column(db.Float)
    r_cost = db.Column(db.Float)
    r_carb = db.Column(db.Float)
    # For alternatives
    r_dish = db.Column(db.Float)
    r_dry = db.Column(db.Float)
    r_heatS = db.Column(db.Float)
    r_heatW = db.Column(db.Float)
    r_coolS = db.Column(db.Float)
    r_coolW = db.Column(db.Float)
    r_showS = db.Column(db.Float)
    r_showW = db.Column(db.Float)
    # Ranks for criteria and alternatives
#    rnk_comf = db.Column(db.Integer)
#    rnk_cost = db.Column(db.Integer)
#    rnk_carb = db.Column(db.Integer)
    rnk_dish = db.Column(db.Integer)
    rnk_dry = db.Column(db.Integer)
    rnk_heatS = db.Column(db.Integer)
    rnk_heatW = db.Column(db.Integer)
    rnk_coolS = db.Column(db.Integer)
    rnk_coolW = db.Column(db.Integer)
    rnk_showS = db.Column(db.Integer)
    rnk_showW = db.Column(db.Integer)
    # length vs. temp
    # heating at home
    r_cool = db.Column(db.String(10))
    # cooling at home
    r_heat = db.Column(db.String(10))
    # shower at home
    r_show = db.Column(db.String(10))
    
    def __init__(self, rwid, zipCode, r_comf, r_cost, r_carb, r_dish, r_dry,
                 r_heatS, r_heatW, r_coolS, r_coolW, r_showS, r_showW, rnk_dish,
                 rnk_dry, rnk_heatS, rnk_heatW, rnk_coolS, rnk_coolW,
                 rnk_showS, rnk_showW, r_cool, r_heat, r_show):        
        self.rwid = rwid
        self.zipCode = zipCode
        self.r_comf = r_comf
        self.r_cost = r_cost
        self.r_carb = r_carb
        self.r_dish = r_dish
        self.r_dry = r_dry
        self.r_heatS = r_heatS
        self.r_heatW = r_heatW
        self.r_coolS = r_coolS
        self.r_coolW = r_coolW
        self.r_showS = r_showS
        self.r_showW = r_showW
#        self.rnk_comf = rnk_comf
#        self.rnk_cost = rnk_cost
#        self.rnk_carb = rnk_carb
        self.rnk_dish = rnk_dish
        self.rnk_dry = rnk_dry
        self.rnk_heatS = rnk_heatS
        self.rnk_heatW = rnk_heatW
        self.rnk_coolS = rnk_coolS
        self.rnk_coolW = rnk_coolW
        self.rnk_showS = rnk_showS
        self.rnk_showW = rnk_showW
        self.r_cool = r_cool
        self.r_heat = r_heat
        self.r_show = r_show
        
# Generate a 6 digit random alphanumeric
def genID(N):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))

# Define a route for the default URL, which loads the form
@app.route('/')
def main():
    # Create a worker id
    rec = {'wid':genID(6)}
    return render_template('index.html', workID = rec)

@app.route('/submitDat', methods = ['GET', 'POST'])
def submitDat():
    if request.method == 'POST':

        # Get the appliance usage info
        if 'dsh_use' in request.form:
            run_dish = request.form['dsh_use']
            dishBool = 'True'
        else:
            run_dish = 30
            dishBool = 'False'
        if 'dr_use' in request.form:
            run_dr = request.form['dr_use']
            drBool = 'True'
        else:
            run_dr = 30
            drBool = 'False'
        if 'shS_use' in request.form:
            run_heatS = request.form['shS_use']
            run_heatW = int(request.form['shW_use'])
            shBool = 'True'
        else:
            run_heatS = 30
            run_heatW = 30
            shBool = 'False'
        if 'acS_use' in request.form:
            run_coolS = request.form['acS_use']
            run_coolW = request.form['acW_use']
            acBool = 'True'
        else:
            run_coolS = 30
            run_coolW = 30
            acBool = 'False' 
        if 'whS_use' in request.form:
            run_showS = request.form['whS_use']
            run_showW = request.form['whW_use']
            whBool = 'True'
        else:
            run_showS = 30
            run_showW = 30
            whBool = 'False'
        if 'chk_wm' in request.form:
            wmBool = 'True'
        else:
            wmBool = 'False'
            
        record = surveyAHP(request.form['workid'], float(request.form['sl_comf']), float(request.form['sl_cost']), float(request.form['sl_carb']),
                           float(request.form['sl_dish']),float(request.form['sl_dry']),float(request.form['sl_heatS']),float(request.form['sl_heatW']),
                           float(request.form['sl_coolS']),float(request.form['sl_coolW']),float(request.form['sl_showS']),float(request.form['sl_showW']),
                           dishBool, run_dish, drBool, run_dr, shBool, run_heatS, run_heatW, acBool, run_coolS, run_coolW,
                           whBool, run_showS, run_showW, wmBool, request.form['coollen'], request.form['heatlen'], request.form['showlen'],
                           str(request.form['txt_age']), str(request.form['txt_zip']), request.form['gender'])
        
        db.session.add(record)
        db.session.commit()
        user = surveyAHP.query.filter_by(wid=request.form['workid']).first_or_404()
        if user.wid != '':
            msg = ' Your response has been successfully recorded.'
        else:
            msg = ' There was an error in your response. Please try again.'
        return jsonify(stat = msg)

@app.route('/batchDat', methods = ['GET', 'POST'])
def batchDat():
    #self, rwid, zipCode, r_comf, r_cost, r_carb, r_dish, r_dry,
    #     r_heatS, r_heatW, r_coolS, r_coolW, r_showS, r_showW, rnk_dish, rnk_dry, rnk_heatS, rnk_heatW, rnk_coolS, rnk_coolW,
    #     rnk_showS, rnk_showW, r_cool, r_heat, r_show
    nm = resAHP.query.with_entities(resAHP.rwid,resAHP.zipCode,resAHP.r_comf,resAHP.r_cost,resAHP.r_carb,resAHP.r_dish,resAHP.r_dry,resAHP.r_heatS,
                                    resAHP.r_heatW,resAHP.r_coolS,resAHP.r_coolW,resAHP.r_showS,resAHP.r_showW,resAHP.rnk_dish,resAHP.rnk_dry,resAHP.rnk_heatS,
                                    resAHP.rnk_heatW,resAHP.rnk_coolS,resAHP.rnk_coolW,resAHP.rnk_showS,resAHP.rnk_showW,resAHP.r_cool,resAHP.r_heat,resAHP.r_show)
    # IDs
    nmList = [nm.rwid for nm in nm.all()]
    zipList = [nm.zipCode for nm in nm.all()]
    comList = [nm.r_comf for nm in nm.all()]
    cosList = [nm.r_cost for nm in nm.all()]
    carList = [nm.r_carb for nm in nm.all()]
    dshList = [nm.r_dish for nm in nm.all()]
    dryList = [nm.r_dry for nm in nm.all()]
    hSList = [nm.r_heatS for nm in nm.all()]
    hWList = [nm.r_heatW for nm in nm.all()]
    cSList = [nm.r_coolS for nm in nm.all()]
    cWList = [nm.r_coolW for nm in nm.all()]
    sSList = [nm.r_showS for nm in nm.all()]
    sWList = [nm.r_showW for nm in nm.all()]
    rdshList = [nm.rnk_dish for nm in nm.all()]
    rdryList = [nm.rnk_dry for nm in nm.all()]
    rhSList = [nm.rnk_heatS for nm in nm.all()]
    rhWList = [nm.rnk_heatW for nm in nm.all()]
    rcSList = [nm.rnk_coolS for nm in nm.all()]
    rcWList = [nm.rnk_coolW for nm in nm.all()]
    rsSList = [nm.rnk_showS for nm in nm.all()]
    rsWList = [nm.rnk_showW for nm in nm.all()]
    cList = [nm.r_cool for nm in nm.all()]
    hList = [nm.r_heat for nm in nm.all()]
    sList = [nm.r_show for nm in nm.all()]    
    index = [i for i in range(len(nmList))]
    
    ahp_res = pd.DataFrame(index=index, columns=['id', 'zip', 'Comfort','Cost','Carbon','Dishwasher', 'Dryer',
                                                 'Heating(S)', 'Heating(W)', 'Cooling(S)', 'Cooling(W)', 'Shower(S)', 'Shower(W)',
                                                 'rnk_dish', 'rnk_dryer', 'rnk_heat(S)', 'rnk_heat(W)', 'rnk_cool(S)', 'rnk_cool(W)',
                                                 'rnk_show(S)', 'rnk_show(W)', 'cool','heat','show'])
    for i in range(len(nmList)):
      ahp_res.loc[i] = [nmList[i], zipList[i], comList[i], cosList[i], carList[i], dshList[i], dryList[i],
                        hSList[i], hWList[i], cSList[i], cWList[i], sSList[i], sWList[i], rdshList[i], rdryList[i],
                        rhSList[i], rhWList[i], rcSList[i], rcWList[i], rsSList[i], rsWList[i], cList[i], hList[i], sList[i]]
      
    if os.path.exists("static/resultAHP.csv"):
        try:
            os.remove("static/resultAHP.csv")
            ahp_res.to_csv("static/resultAHP.csv")
        except:
            pass
    else:
        ahp_res.to_csv("static/resultAHP.csv")

    # Remove all the plot files
    clrpng = glob.glob("static/*.png")
    for f in clrpng:
        os.remove(f)
        
    # Generate the correlation heatmap for the criteria
    p1 = corrAHP("static/resultAHP.csv", c_nm, "Cri_Corr"+genID(2))

    # Generate the correlation heatmap for the alternatives
    p2 = corrAHP("static/resultAHP.csv", a_nm, "App_weights_Corr"+genID(2))             

    # Generate the appliance rank plot
    p3 = rnkAHP("static/resultAHP.csv", "App_rnk"+genID(2))
 

    return jsonify(stat1=p1,stat2=p2,stat3=p3)

@app.route('/getuserDat', methods = ['GET', 'POST'])
def getuserDat():
    if request.method == 'POST':
        nm = surveyAHP.query.with_entities(surveyAHP.wid)
        uList = [nm.wid for nm in nm.all()]
    return jsonify(ulist=uList)

@app.route('/getzipDat', methods = ['GET', 'POST'])
def getzipDat():
    if request.method == 'POST':
        par0 = request.form['opt0']
        par1 = request.form['opt1']
        par2 = request.form['opt2']
        if par2 == '1':
            par2 = int(par2)
            
        fl = mapAHP("static/resultAHP.csv", [par0, par1, par2], "zipPlot"+genID(2))
        
    return jsonify(stat=fl)
        
@app.route('/processDat', methods = ['GET', 'POST'])
def processDat():
    
    if request.method == 'POST':
        # Process the AHP code from the db
        user = surveyAHP.query.filter_by(wid=str(request.form['recid'])).first_or_404()

        #nm = surveyAHP.query.with_entities(surveyAHP.wid)
        #uList = [nm.wid for nm in nm.all()]
        
        # Criterion values
        comf = float(user.sl_comf)
        cost = float(user.sl_cost)
        carb = float(user.sl_carb)
        cdat = [comf,cost,carb]

        # Perform AHP for the criteria
        pwMat,priC,cr = createAHP(cdat)
        priC = priC.tolist()
        cri_clr = clrRnk(priC)
        cri_pri = {'comf':str(round(priC[0],3)), 'cost':str(round(priC[1],3)), 'carb':str(round(priC[2],3)), 'ccr': str(round(cr*100,3)), 'criclr':cri_clr}

        # Alternatives values
        dish = float(user.sl_dish)
        dry = float(user.sl_dry)
        heatS = float(user.sl_heatS)
        heatW = float(user.sl_heatW)
        coolS = float(user.sl_coolS)
        coolW = float(user.sl_coolW)
        showS = float(user.sl_showS)
        showW = float(user.sl_showW)         
        adat_f = [dish,dry,heatS,heatW,coolS,coolW,showS,showW]

        # Perform AHP for the alternatives - FUNCTIONALITY
        priA = []
        pwMat,priF,cr = createAHP(adat_f)
        priA.append(priF.tolist())

        at_f_pri = {'dish':str(priF[0]), 'dry':str(priF[1]), 'heatS':str(priF[2]), 'heatW':str(priF[3]),
                    'coolS':str(priF[4]), 'coolW':str(priF[5]), 'showS':str(priF[6]), 'showW':str(priF[7]), 'acr':str(round(cr*100,3))}

        # Appliances runtime
        app_list = []
        run_dish = int(user.run_dish)
        run_dr = int(user.run_dr)
        run_heatS = int(user.run_heatS)
        run_heatW = int(user.run_heatW)
        run_coolS = int(user.run_coolS)
        run_coolW = int(user.run_coolW)
        run_showS = int(user.run_showS)
        run_showW = int(user.run_showW)        
        if user.dsh_use == 'True':            
            app_list.append('Dishwasher')
        if user.dr_use == 'True':
            app_list.append('Dryer')
        if user.sh_use == 'True':
            app_list.append('Space Heater')
        if user.ac_use == 'True':
            app_list.append('Air Conditioner')
        if user.wh_use == 'True':
            app_list.append('Water Heater')
        if user.wm_use == 'True':
            app_list.append('Washing Machine')
            
        adat = [run_dish,run_dr,run_heatS,run_heatW,run_coolS,run_coolW,run_showS,run_showW]
        arun = [30 if adat[i] == 0 else adat[i] for i in range(len(adat))]
        
        temp = {'dwrun':str(arun[0]),'drrun':str(arun[1]),'hSrun':str(arun[2]),
                'hWrun':str(arun[3]),'cSrun':str(arun[4]),'cWrun':str(arun[5]),
                'sSrun':str(arun[6]),'sWrun':str(arun[7])}

        # Perform AHP for the alternatives - COST
        cost = []
        for i in range(len(a)):
            cost.append([appCost(a[i],arun[i],u_rate,app_def)])        
        cost1 = listflat(cost)
        cost = C_to_AHP(cost1)
        
        pwMat,priCt,cr = createAHP(cost)
        priA.append(priCt.tolist())
        
        at_Ct_pri = {'dish':str(priCt[0]), 'dry':str(priCt[1]), 'heatS':str(priCt[2]), 'heatW':str(priCt[3]),
                    'coolS':str(priCt[4]), 'coolW':str(priCt[5]), 'showS':str(priCt[6]), 'showW':str(priCt[7]), 'acr':str(round(cr*100,3))}
        
        # Perform AHP for the alternatives - CARBON
        carbon = []
        for i in range(len(a)):
            carbon.append([appCrbn(a[i],arun[i],app_def)])       
        carbon = listflat(carbon)
        carbon = C_to_AHP(carbon)
        
        pwMat,priCr,cr = createAHP(carbon)
        priA.append(priCr.tolist())
        cri_clr = clrRnk(priC)
        # Compute the final ranking
        res,rnk = computeRank(priA,priC,a)
        at_Cr_pri = {'dish':str(priCr[0]), 'dry':str(priCr[1]), 'heatS':str(priCr[2]), 'heatW':str(priCr[3]),
                    'coolS':str(priCr[4]), 'coolW':str(priCr[5]), 'showS':str(priCr[6]), 'showW':str(priCr[7]), 'acr':str(round(cr*100,3))}
        
        app_res = {'dish':str(round(res[0],3)), 'dry':str(round(res[1],3)), 'heatS':str(round(res[2],3)), 'heatW':str(round(res[3],3)),
                    'coolS':str(round(res[4],3)), 'coolW':str(round(res[5],3)), 'showS':str(round(res[6],3)), 'showW':str(round(res[7],3)), 'resclr':clrRnk(res)}
        
        app_rnk = {'dish':str(rnk[0]), 'dry':str(rnk[1]), 'heatS':str(rnk[2]), 'heatW':str(rnk[3]),
                    'coolS':str(rnk[4]), 'coolW':str(rnk[5]), 'showS':str(rnk[6]), 'showW':str(rnk[7]), 'rnkclr':clrRnk(rnk)}

        # Case scenario
        if user.coollen == 'coollen1':
            coolmsg = 'temp'
        elif user.coollen == 'coollen2':
            coolmsg = 'len'
        else:
            coolmsg = 'No pref'
        if user.heatlen == 'heatlen1':
            heatmsg = 'temp'
        elif user.heatlen == 'heatlen2':
            heatmsg = 'len'    
        else:
            heatmsg = 'No pref'
        if user.showlen == 'showlen1':
            showmsg = 'temp'
        elif user.showlen == 'showlen2':
            showmsg = 'len'    
        else:
            showmsg = 'No pref'            
        app_scn = {'cool':str(coolmsg),'heat':str(heatmsg),'show':str(showmsg)}

        # Submit the AHP result to db
        if resAHP.query.filter_by(rwid=str(request.form['recid'])).first():
            stat = 'result exists'
        else:
            stat = 'result submitted'
            record = resAHP(user.wid, user.zipCode, float(cri_pri['comf']), float(cri_pri['cost']), float(cri_pri['carb']),
                            float(app_res['dish']), float(app_res['dry']), float(app_res['heatS']), float(app_res['heatW']),
                            float(app_res['coolS']), float(app_res['coolW']), float(app_res['showS']), float(app_res['showW']),
                            int(app_rnk['dish']), int(app_rnk['dry']), int(app_rnk['heatS']), int(app_rnk['heatW']),
                            int(app_rnk['coolS']), int(app_rnk['coolW']), int(app_rnk['showS']), int(app_rnk['showW']),
                            str(app_scn['cool']), str(app_scn['heat']), str(app_scn['show']))
            
            db.session.add(record)
            db.session.commit()
        
    return jsonify(cri=cri_pri, alf=at_f_pri, alCt=at_Ct_pri, alCr=at_Cr_pri,
                   app=app_list, apprun=temp, appres = app_res, apprnk = app_rnk, appscn = app_scn, reChk = stat)#,ulist=uList) #Ct = cost1, scaleCt=cost)

def clrRnk(lst):
    lst_clr = ['#009900' if lst[i] == min(lst) else '#CC0000' if lst[i] == max(lst) else '#000000' for i in range(len(lst))]
    key = ['clr'+str(i) for i in range(len(lst))]
    d = zip(key,lst_clr)
    dic_clr = dict(d)
    return collections.OrderedDict(sorted(dic_clr.items()))
    
# Run the app :)
if __name__ == '__main__':
    
    db.create_all()    
    app.run( 
        #host="0.0.0.0",
        port=int("5002"),
        #debug=True
    )
