from flask import render_template, flash, redirect, request, url_for, session, g
from app import app
from .forms import LoginForm, RegisterForm, NewPostForm
from datetime import datetime
import requests
from lxml import etree

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = NewPostForm()
    if form.validate_on_submit:
        print form
    data = {"data": make_ship_request()}
    return render_template('index.html',
                            title='Home',
                            data=data)

@app.route('/results')
def results():
    return render_template('results.html', results = [1,2,3,4,5])

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/time')
def time():
    sessionkey = session["sessionkey"]
    cabin_grade_request(sessionkey)
    return render_template('time.html')

def get_session_key(sessionkey):
    root = etree.fromstring(r.text)
    data = {}
    for child in root.iterfind("request/method"):
        session["sessionkey"] = child.get("sessionkey")
        break
    return data


def cabin_grade_request(sessionkey):
    request = """
        <request>
          <auth username="hackathon" password="pr38ns48" />
          <method action="getcabingrades" sessionkey="{0}" resultno="{1}" />
        </request>
    """.format(sessionkey, "302_25.0")

    url = "http://fusionapi.traveltek.net/0.9/interface.pl"
    r = requests.post(url, data={"xml": request})
    root = etree.fromstring(r.text)
    print "******"
    import xmltodict, json

    o = xmltodict.parse(r.text)
    json = json.dumps(o)
    a = json.parse(json)
    print a["response"]["results"]["grades"]



def make_ship_request():

    line17Request = """<?xml version="1.0"?>
    <request>
        <auth username="hackathon" password="pr38ns48" />
        <method action="getlinecontent" lineid="17"/>
    </request>"""

    line22Request = """<?xml version="1.0"?>
    <request>
        <auth username="hackathon" password="pr38ns48" />
        <method action="getlinecontent" lineid="22"/>
    </request>"""

    #print test_request
    url = "http://fusionapi.traveltek.net/0.9/interface.pl"
    line17 = requests.post(url, data={"xml": line17Request})
    line22 = requests.post(url, data={"xml": line22Request})

    # parse

    line17Tree = etree.fromstring(line17.text)
    line22Tree = etree.fromstring(line22.text)
    #print line17.text
    #print line22.text

    shipList = []
    # loop and print hotel name
    for element in line17Tree.iterfind("results/line/ships/ship"):
        #print element.get("session")
        name = element.get("name")
        print name
        #desc = element.get("description")
        shipList.append(name)
    for element in line22Tree.iterfind("results/line/ships/ship"):
        name=element.get("name")
        print name
        shipList.append(name)

    shipList = sorted(shipList)
    return shipList

def make_full_search():
    searchCriteria = "<searchdetail"
    #region = form.data
