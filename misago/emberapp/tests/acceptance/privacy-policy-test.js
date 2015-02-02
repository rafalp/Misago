import Ember from 'ember';
import startApp from '../helpers/start-app';

var application;

module('Acceptance: PrivacyPolicy', {
  setup: function() {
    application = startApp();
  },
  teardown: function() {
    Ember.run(application, 'destroy');
    Ember.$.mockjax.clear();
  }
});

test('visiting unset /privacy-policy', function() {
  Ember.$.mockjax({
    url: "/api/legal-pages/privacy-policy/",
    status: 404,
    responseText: {'detail': 'Not found'}
  });

  visit('/privacy-policy');

  andThen(function() {
    equal(currentPath(), 'error-404');
  });
});

test('visiting set /privacy-policy', function() {
  Ember.$.mockjax({
    url: "/api/legal-pages/privacy-policy/",
    status: 200,
    responseText: {
      'id': 'privacy-policy',
      'title': 'Privacy policy',
      'link': '',
      'body': '<p>Top kek</p>'
    }
  });

  visit('/privacy-policy');

  andThen(function() {
    equal(currentPath(), 'privacy-policy');
    var $e = find('article');
    equal(Ember.$.trim($e.html()), '<p>Top kek</p>');
  });
});
