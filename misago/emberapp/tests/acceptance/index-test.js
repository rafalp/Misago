import Ember from 'ember';
import startApp from '../helpers/start-app';

var application;

module('Acceptance: Index', {
  setup: function() {
    application = startApp();
  },
  teardown: function() {
    Ember.run(application, 'destroy');
  }
});

test('visiting /', function() {
  visit('/');

  andThen(function() {
    equal(currentPath(), 'index');
  });
});

test('visiting / with custom title', function() {
  var newTitle = "Misago Support Forums";
  window.MisagoData.misagoSettings['forum_index_title'] = newTitle;
  visit('/');

  andThen(function() {
    equal(currentPath(), 'index');
    equal(document.title, newTitle);
  });
});
