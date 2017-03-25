from flask import render_template, flash, redirect, request, url_for, session, g
from app import app
from .forms import LoginForm, RegisterForm, NewPostForm, RegionForm, TimeForm, BoatForm
from datetime import datetime
import requests
from lxml import etree

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = NewPostForm()
    if form.validate_on_submit:
        print form

    return render_template('index.html',
                            title='Home')

@app.route('/steps', methods=['GET', 'POST'])
def steps():
    return render_template('steps.html')


@app.route('/results')
def results():
    results = make_full_search()
    images =["/static/more.jpeg", "/static/other.jpeg", "/static/images.jpeg", "http://static.traveltek.net/cruisepics/local_shipimages_small/1423568677.jpg"]
    import random
    for item in results:
        item.append(random.choice(images))
    results = sorted(results, reverse=True)
    return render_template('results.html', results=results)

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


    shipList = {}
    for element in line17Tree.iterfind("results/line/ships/ship"):
        name = element.get("name")
        ID = element.get("id")
        shipList[name] = ID

    for element in line22Tree.iterfind("results/line/ships/ship"):
        name=element.get("name")
        ID = element.get("id")
        shipList[name] = ID

    shipList = sorted(shipList)
    return shipList

def make_full_search():


    regionForm = RegionForm()
    timeForm = TimeForm()
    boatForm = BoatForm()
    shipList = make_ship_request()
    regionList = {"Africa":17,
                "Alaska":13,
                "Asia & Indian Ocean":5,
                "Australasia":14,
                "Bahamas":28,
                "Baltic":20,
                "Bermuda":21,
                "Black Sea":21,
                "Canaries":1,
                "Caribbean":2,
                "Central America":3,
                "China":24,
                "Dubai & Emirates":23,
                "Egypt & Red Sea":25,
                "Europe":4,
                "Fiji":32,
                "Hawaii":6,
                "Iberian Peninsula":22,
                "Mediterranean":7,
                "Mexico":26,
                "Middle East":19,
                "North America":8,
                "Pacific":15,
                "Panama Canal":31,
                "Polar Regions":18,
                "Russia":29,
                "Scandinavia":9,
                "South America":10,
                "Transatlantic":11,
                "United Kingdom":16,
                "Worldwide":12}


    region = "Caribbean"
    startDate = None
    endDate = None
    boat = None

    searchCriteria = "<searchdetail sid=\"30115\" type=\"cruise\" resultkey=\"default\" startdate=\"2017-03-25\" enddate=\"2017-04-08\" adults=\"2\" children=\"0\""

    if (region != None):
        searchCriteria = searchCriteria + " regionid=" + "\"" + str(regionList[region]) + "\""
    if (boat != None):
        searchCriteria = searchCriteria + " shipid=" + "\"" + shipList[ship] + "\""

    searchCriteria = searchCriteria + " >"

    fullRequest = """<?xml version="1.0"?>
    <request>
        <auth username="hackathon" password="pr38ns48" />
        <method action="simplesearch" sitename="cruisedemo.traveltek.net"
            status="Live" type="cruise"> \n""" + searchCriteria + """\n
        </searchdetail>
        </method>
    </request>"""

    print fullRequest

    url = "http://fusionapi.traveltek.net/0.9/interface.pl"
    searchResults = requests.post(url, data={"xml": fullRequest})

    searchTree = etree.fromstring(searchResults.text)
    print searchResults.text
    cruises = []
    for element in searchTree.iterfind("results/cruise"):
        name = element.get("name")
        currency = element.get("currency")
        price = element.get("price")
        engine = element.get("engine")
        #regionid = element.get("regionid")

        cruises.append([name, currency, price, engine])#regionList.keys()[regionList.values().index(regionid)]])


    return cruises
