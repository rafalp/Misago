import Ember from 'ember';
import { module, test } from 'qunit';
import startApp from '../helpers/start-app';

var application;

module('Acceptance: TermsOfService', {
  beforeEach: function() {
    application = startApp();
  },
  afterEach: function() {
    Ember.run(application, 'destroy');
    Ember.$.mockjax.clear();
  }
});

test('visiting unset /terms-of-service', function(assert) {
  assert.expect(1);

  Ember.$.mockjax({
    url: '/api/legal-pages/terms-of-service/',
    status: 404,
    responseText: {'detail': 'Not found'}
  });

  visit('/terms-of-service');

  andThen(function() {
    assert.equal(currentPath(), 'error-404');
  });
});

test('visiting set /terms-of-service', function(assert) {
  assert.expect(2);

  Ember.$.mockjax({
    url: '/api/legal-pages/terms-of-service/',
    status: 200,
    responseText: {
      'id': 'terms-of-service',
      'title': 'Terms of service',
      'link': '',
      'body': '<p>Terms of service are working!</p>'
    }
  });

  visit('/terms-of-service');

  andThen(function() {
    assert.equal(currentPath(), 'terms-of-service');
    var $e = find('article');
    assert.equal(Ember.$.trim($e.html()), '<p>Terms of service are working!</p>');
  });
});
