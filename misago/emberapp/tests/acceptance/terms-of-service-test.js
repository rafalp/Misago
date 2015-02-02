import Ember from 'ember';
import startApp from '../helpers/start-app';

var application;

module('Acceptance: TermsOfService', {
  setup: function() {
    application = startApp();
  },
  teardown: function() {
    Ember.run(application, 'destroy');
    Ember.$.mockjax.clear();
  }
});

test('visiting unset /terms-of-service', function() {
  Ember.$.mockjax({
    url: "/api/legal-pages/terms-of-service/",
    status: 404,
    responseText: {'detail': 'Not found'}
  });

  visit('/terms-of-service');

  andThen(function() {
    equal(currentPath(), 'error-404');
  });
});

test('visiting set /terms-of-service', function() {
  Ember.$.mockjax({
    url: "/api/legal-pages/terms-of-service/",
    status: 200,
    responseText: {
      'id': 'terms-of-service',
      'title': 'Terms of service',
      'link': '',
      'body': '<p>Top kek</p>'
    }
  });

  visit('/terms-of-service');

  andThen(function() {
    equal(currentPath(), 'terms-of-service');
    var $e = find('article');
    equal(Ember.$.trim($e.html()), '<p>Top kek</p>');
  });
});
