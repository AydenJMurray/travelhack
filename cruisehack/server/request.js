import { Meteor } from 'meteor/meteor'

Meteor.methods({
  apiRequest: function ()
  {
    this.unblock();
    console.log("Method Called");
    var xmlRequest = `<?xml version="1.0"?>
                      <request>
                      <auth username="hackathon" password="pr38ns48" />
                      <method action="simplesearch" sitename="cruisedemo.traveltek.net"
                      status="Live" type="cruise">
                      <searchdetail type="cruise" startdate="2017-04-01" enddate="2017-04-30"
                      adults="2" children="0" sid="30115" resultkey="default">
                      </searchdetail>
                      </method>
                      </request>`;
    var apiUrl = "https://fusionapi.traveltek.net/0.9/interface.pl";


    return Meteor.http.post(apiUrl, {params: {xml:xmlRequest}});

  }
});
