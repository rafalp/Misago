import Ember from 'ember';
import { module, test } from 'qunit';
import startApp from '../helpers/start-app';

var application;

module('Acceptance: Application Error Handler', {
  beforeEach: function() {
    application = startApp();
  },
  afterEach: function() {
    Ember.run(application, 'destroy');
    Ember.$.mockjax.clear();
  }
});

test('some unhandled error occured', function(assert) {
  assert.expect(1);

  Ember.$.mockjax({
    url: '/api/legal-pages/privacy-policy/',
    status: 500,
    responseText: {
      'detail': 'Some terrible Django error'
    }
  });

  visit('/privacy-policy');

  andThen(function() {
    assert.equal(currentPath(), 'error');
  });
});

test('app went away', function(assert) {
  assert.expect(1);

  Ember.$.mockjax({
    url: '/api/legal-pages/privacy-policy/',
    status: 0,
    responseText: {
      'detail': 'Connection rejected'
    }
  });

  visit('/privacy-policy');

  andThen(function() {
    assert.equal(currentPath(), 'error-0');
  });
});

test('not found', function(assert) {
  assert.expect(1);

  Ember.$.mockjax({
    url: '/api/legal-pages/privacy-policy/',
    status: 404,
    responseText: {
      'detail': 'Not found'
    }
  });

  visit('/privacy-policy');

  andThen(function() {
    assert.equal(currentPath(), 'error-404');
  });
});

test('permission denied', function(assert) {
  assert.expect(1);

  Ember.$.mockjax({
    url: '/api/legal-pages/privacy-policy/',
    status: 403,
    responseText: {
      'detail': 'Permission denied'
    }
  });

  visit('/privacy-policy');

  andThen(function() {
    assert.equal(currentPath(), 'error-403');
  });
});

test('permission denied with reason', function(assert) {
  assert.expect(2);

  Ember.$.mockjax({
    url: '/api/legal-pages/privacy-policy/',
    status: 403,
    responseText: {
      'detail': 'Lorem ipsum dolor met.'
    }
  });

  visit('/privacy-policy');

  andThen(function() {
    assert.equal(currentPath(), 'error-403');
    var $e = find('.lead');
    assert.equal(Ember.$.trim($e.text()), 'Lorem ipsum dolor met.');
  });
});

test('banned', function(assert) {
  assert.expect(3);

  Ember.$.mockjax({
    url: '/api/legal-pages/privacy-policy/',
    status: 403,
    responseText: {
      'ban': {
        'expires_on': null,
        'message': {
          'plain': 'You are banned.',
          'html': '<p>You are banned.</p>'
        }
      }
    }
  });

  visit('/privacy-policy');

  andThen(function() {
    assert.equal(currentPath(), 'error-banned');

    var errorMessage = find('.lead p').text();
    assert.equal(errorMessage, 'You are banned.');

    var expirationMessage = find('.error-message>p').text();
    assert.equal(expirationMessage, 'This ban is permanent.');
  });
});

test('not found route', function(assert) {
  assert.expect(1);

  visit('/this-url-really-doesnt-exist');

  andThen(function() {
    assert.equal(currentPath(), 'error-404');
  });
});
