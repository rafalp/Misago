import Ember from 'ember';
import { module, test } from 'qunit';
import startApp from '../helpers/start-app';

var application;

module('Acceptance: PrivacyPolicy', {
  beforeEach: function() {
    application = startApp();
  },
  afterEach: function() {
    Ember.run(application, 'destroy');
    Ember.$.mockjax.clear();
  }
});

test('visiting unset /privacy-policy', function(assert) {
  Ember.$.mockjax({
    url: "/api/legal-pages/privacy-policy/",
    status: 404,
    responseText: {'detail': 'Not found'}
  });

  visit('/privacy-policy');

  andThen(function() {
    assert.equal(currentPath(), 'error-404');
  });
});

test('visiting set /privacy-policy', function(assert) {
  Ember.$.mockjax({
    url: "/api/legal-pages/privacy-policy/",
    status: 200,
    responseText: {
      'id': 'privacy-policy',
      'title': 'Privacy policy',
      'link': '',
      'body': '<p>Privacy policy is working!</p>'
    }
  });

  visit('/privacy-policy');

  andThen(function() {
    assert.equal(currentPath(), 'privacy-policy');
    var $e = find('article');
    assert.equal(Ember.$.trim($e.html()), '<p>Privacy policy is working!</p>');
  });
});
