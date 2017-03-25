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
    data = {"data": make_request()}
    return render_template('index.html',
                            title='Home',
                            data=data)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/time')
def time():
    sessionkey = session["sessionkey"]
    print sessionkey
    return render_template('time.html')


def make_request():
    test_request = """
        <request>
         <auth username="hackathon" password="pr38ns48" />
         <method action="simplesearch" sitename="cruisedemo.traveltek.net"
            status="Live" type="cruise">
          <searchdetail type="cruise" startdate="2017-04-01" enddate="2017-04-30"
            adults="2" children="0" sid="30115" resultkey="default">
          </searchdetail>
         </method>
        </request>
        """

    #print test_request
    url = "http://fusionapi.traveltek.net/0.9/interface.pl"
    r = requests.post(url, data={"xml": test_request})

    # parse
    root = etree.fromstring(r.text)

    data = {}
    for child in root.iterfind("request/method"):
        session["sessionkey"] = child.get("sessionkey")
        break

    return data
