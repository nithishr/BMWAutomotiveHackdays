__author__ = 'nithishr'
import pymongo
from app import app
from flask import render_template, request, redirect, url_for
import usersDAO
import deliverersDAO
import requestsDAO
import googlemaps
import smtplib
import paho.mqtt.client as paho

userLoggedIn = 'arnold'
currentRequest = '56f0f2e49b044a15b5ebb513'

client = paho.Client()
# client.on_publish = on_publish
client.connect("hackdays.hivemq.com", 1883)
client.loop_start()

def sendMail(recipient='nithishr@gmail.com',req_id='test'):
    seed ="Trunknow22"
    GMAIL_USERNAME = 'mytrunknow@gmail.com'
    email_subject = 'TrunkNow Delivery'
    headers = "\r\n".join(["from: " + GMAIL_USERNAME,
                       "subject: " + email_subject,
                       "to: " + recipient,
                       "mime-version: 1.0",
                       "content-type: text/html"])
    body_of_email = r"Your package " + req_id + " just got delivered."
    content = headers + "\r\n\r\n" + body_of_email
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(GMAIL_USERNAME,seed)
    server.sendmail(GMAIL_USERNAME, recipient, content)
    server.quit()

def sendMQTTMessage(code):
    global client
    publisher = "BMW/FIZcar/HACKATHON_2D78918/test/pub"
    publisher = "BMW/FIZcar/HACKATHON_2D78918/business/downlink"
    (rc,mid)=client.publish(publisher, code, qos=2)

def geoLookup(address='Lichtenbergstrasse 6, D-85748 Garching'):
    # Replace the API key below with a valid API key.
    gmaps = googlemaps.Client(key='AIzaSyCsbJPB6b7c62jkKtHzSV23AkA5uqVnBbc')
    # Geocoding and address
    geocode_result = gmaps.geocode(address)
    location = geocode_result[-1]['geometry']['location']
    latitude = location['lat']
    longitude = location['lng']
    return location

@app.route('/demo')
@app.route('/')
@app.route('/index')
def index():
    # user = {'nickname': 'TrunkNow'}  # fake user
    # return render_template('index.html',
    #                        title='Home',
    #                        user=user)
    return render_template('index.html')
                           #title='Home',
                           #user=user)
    # return "Welcome to TrunkNow"

@app.route('/user/<username>')
def user(username=''):
    global userLoggedIn
    userLoggedIn = username
    # return "Hello "+username+' '+ str(users.getUseridFromName(username))
    uid = str(users.getUseridFromName(username))
    userd={'username':username,'uid':uid}
    return render_template('user.html', u=userd)#un=username, uid=uid)

@app.route('/delivery/<dlid>')
def deliver(dlid=''):
    packages = requestDB.filterRequests({'delId':dlid})
    lst = []
    for package in packages:
        # print str(package)
        lst.append(package)
    return render_template('deliverer.html',packs=lst)
    # return "Hello "+dlid#+' '+ str(users.getUseridFromName(username))
    # uid = str(users.getUseridFromName(username))
    # userd={'username':username,'uid':uid}
    # return render_template('user.html', u=userd)#un=username, uid=uid)

@app.route('/identify-car')
def idCar(req_id=''):
    print "hello car"
    global currentRequest
    sendMQTTMessage('i')
    # return "hello car"
    return redirect('/request/'+currentRequest)

@app.route('/opentrunk')
def openTrunk(req_id=''):
    print "open car"
    global currentRequest
    sendMQTTMessage('o')
    # sendMail(req_id=req_id)
    print "Req",currentRequest
    # lst = []
    # res = requestDB.filterRequests({'id':currentRequest})
    # for r in res:
    #     lst.append(r)
    # print "r",lst[0]
    requestDB.updateRequest(currentRequest)
    # return "hello car"
    return redirect('/request/'+currentRequest)

@app.route('/location/<loc_id>')
def location(loc_id=''):
    locList=loc_id.split('_')
    loc={'lat':locList[0],'lng':locList[1]}
    # print loc
    return render_template('location.html',location=loc)

@app.route('/request/<req_id>')
def requestId(req_id=''):
    global currentRequest
    currentRequest = req_id
    res = requestDB.filterRequests({'id':req_id})
    lst = []
    for r in res:
        lst.append(r)
    loc= lst[-1]['location']
    st = lst[-1]['status']
    print lst,loc
    # return "hello"
    return render_template('requests.html',req=lst,location=loc,status=st)

@app.route('/demo-request')
def createDemoReq():
    userid = users.getUseridFromName('test')
    location='Lichtenbergstrasse 6, D-85748 Garching'
    delId='DHL_Test'
    # createRequest(self,userid,delId,location,time,date,duration):
    reqId = requestDB.createRequest(userid,delId,geoLookup(location),None, None, None)
    print str(reqId)
    users.addRequest(userLoggedIn,reqId)
    # return redirect('/request/'+str(reqId))
    # return 'localhost:5000/request/'+str(reqId)
    rL = '../request/'+str(reqId)
    return render_template('RequestCreated.html',reqLink=rL)

@app.route('/request',methods = ['POST'])
def createRequest():
    global userLoggedIn
    # print "N:",userLoggedIn
    # print str(request.form['did']),str(request.form['email']), str(request.form['date']), str(request.form['time']), str(request.form['location'])
    # print str(geoLookup(str(request.form['location'])))
    userid = users.getUseridFromName(userLoggedIn)
    reqId = requestDB.createRequest(userid,request.form['did'],geoLookup(str(request.form['location'])),request.form['time'],
                           request.form['date'],request.form['duration'])
    # print str(request.path)
    users.addRequest(userLoggedIn,reqId)
    # print '/user/'+userLoggedIn
    return redirect('/user/'+userLoggedIn)
    # return redirect(url_for('user/'+userLoggedIn))

connection_string = "mongodb://localhost"
connection = pymongo.MongoClient(connection_string)
database = connection.trunkNow

users = usersDAO.UserDAO(database)
deliveries = deliverersDAO.DeliveryDAO(database)
requestDB = requestsDAO.requestsDAO(database)