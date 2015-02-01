from twilioMaps import *
import re
 
from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
 
from twilio import twiml
from twilio.util import TwilioCapability

import forecastio

from geopy import geocoders

import twilioMaps
 
# Declare and configure application
app = Flask(__name__, static_url_path='/static')
app.config.from_pyfile('local_settings.py')
 
 
# Voice Request URL
@app.route('/voice', methods=['GET', 'POST'])
def voice():
    response = twiml.Response()
    response.say("Congratulations! You deployed the Twilio Hackpack "
                 "for Heroku and Flask.")
    return str(response)
 
 
@app.route('/sms', methods=['POST'])
def sms():
    response = twiml.Response()
    body = request.form['Body']
    bodyList = body.split( )
    f = ""
    toCity =""
    to = ""
    i = 1
    city =""
    country = ""
    j = 1
    api_key = "73d4e3aa68e68f9d169121c88304c3dd"
    
    for k in range (0, len(bodyList)):
        bodyList[k] = bodyList[k].lower()
    if bodyList[0] == "gmail":
        if bodyList[1] == "read":
            if len(bodyList) == 2:
                respons = "read first 10"
            elif bodyList[2].isdigit():
                respons = "read full certain email"
            else:
                respons = "error, gmail reading not recognized"
        elif bodyList[1] == "reply":
            if bodyList[2].isdigit():
                respons = "respond to certain email"
            else:
                respons = "error, gmail reading not recognized"
        elif bodyList[1] == "to":
            if "@" in bodyList[2]:
                respons = "send to email"
            else:
                respons = "invalid email"
    elif bodyList[0] == "directions":
        if bodyList[i] != "to":
            while i<len(bodyList) and bodyList[i] != "to":
                f += bodyList[i] + " "
                i+=1
            i+=1
            while i<len(bodyList) and bodyList[i] != ",":
                toCity += bodyList[i] + " "
                i+=1
            i+= 1
            while i<len(bodyList):
                to += bodyList[i] + " "
                i+=1
            bob = Directions(f,toCity,to)
            string = bob.printDirections()
            if(len(string)>1000):
                respons = string[0:1000]
            else:
                respons = string
        else:
            respons = "error, directions reading not recognized"
    elif bodyList[0] == "weather":
        if bodyList[1] != ",":
            while j<len(bodyList) and bodyList[j] != ",":
                city += bodyList[j]
                j+=1
            gn = geocoders.GeoNames(country, "d22hong")
            lat = gn.geocode(city,True) [1] [0];
            long = gn.geocode(city,True) [1] [1];
            forecast = forecastio.load_forecast(api_key, lat, long)
            respons = forecast.currently().summary + " " + str(forecast.currently().temperature) + " C"
    elif bodyList[0] == "news":
        respons ="get news"
    else:
        respons = "error wtf are you doing"
    response.sms(respons)
    return str(response)
 
 
# Twilio Client demo template
@app.route('/client')
def client():
    configuration_error = None
    for key in ('TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN', 'TWILIO_APP_SID',
                'TWILIO_CALLER_ID'):
        if not app.config.get(key, None):
            configuration_error = "Missing from local_settings.py: " \
                                  "{0}".format(key)
            token = None
 
    if not configuration_error:
        capability = TwilioCapability(app.config['TWILIO_ACCOUNT_SID'],
                                      app.config['TWILIO_AUTH_TOKEN'])
        capability.allow_client_incoming("joey_ramone")
        capability.allow_client_outgoing(app.config['TWILIO_APP_SID'])
        token = capability.generate()
    params = {'token': token}
    return render_template('client.html', params=params,
                           configuration_error=configuration_error)
 
 
@app.route('/client/incoming', methods=['POST'])
def client_incoming():
    try:
        from_number = request.values.get('PhoneNumber', None)
 
        resp = twiml.Response()
 
        if not from_number:
            resp.say("Your app is missing a Phone Number. "
                     "Make a request with a Phone Number to make outgoing "
                     "calls with the Twilio hack pack.")
            return str(resp)
 
        if 'TWILIO_CALLER_ID' not in app.config:
            resp.say(
                "Your app is missing a Caller ID parameter. "
                "Please add a Caller ID to make outgoing calls with Twilio "
                "Client")
            return str(resp)
 
        with resp.dial(callerId=app.config['TWILIO_CALLER_ID']) as r:
            # If we have a number, and it looks like a phone number:
            if from_number and re.search('^[\d\(\)\- \+]+$', from_number):
                r.number(from_number)
            else:
                r.say("We couldn't find a phone number to dial. Make sure "
                      "you are sending a Phone Number when you make a "
                      "request with Twilio Client")
        return str(resp)
    except:
        resp = twiml.Response()
        resp.say("An error occurred. Check your debugger at twilio dot com "
                 "for more information.")
        return str(resp)
 
 
# Installation success page
@app.route('/')
def index():
    params = {
        'Voice Request URL': url_for('.voice', _external=True),
        'SMS Request URL': url_for('.sms', _external=True),
        'Client URL': url_for('.client', _external=True)}
    return render_template('index.html', params=params,
                           configuration_error=None)
