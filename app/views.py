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
    return render_template('index.html',
                            title='Home')

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

    # loop and print hotel name
    for element in root.iterfind("results/cruise"):
        print element
        name = element.get("name")
        price = element.get("price")
        return "{0} is {1}".format(name, price)
        
