import { Template } from 'meteor/templating';
import { ReactiveVar } from 'meteor/reactive-var';
import { Mongo } from 'meteor/mongo'

Router.configure({
  layoutTemplate: "layoutDefault",
	notFoundTemplate: "notFound",
	loadingTemplate: "loading"
})

Template.hello.onCreated(function helloOnCreated() {
  
});

Template.hello.helpers({
  counter() {
    return Template.instance().counter.get();
  },
});

Template.hello.events({
  'click button'(event) {

  },
});
