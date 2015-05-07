import Ember from 'ember';
import { module, test } from 'qunit';
import startApp from '../helpers/start-app';
import getToastMessage from '../helpers/toast-message';

var application;

module('Acceptance: Toasting Error Handler', {
  beforeEach: function() {
    application = startApp();
  },
  afterEach: function() {
    Ember.$('#appModal').off();
    Ember.$('body').removeClass('modal-open');
    Ember.run(application, 'destroy');
    Ember.$.mockjax.clear();
  }
});

test('some unhandled error occured', function(assert) {
  assert.expect(1);

  Ember.$.mockjax({
    url: '/api/auth/',
    status: 500
  });

  visit('/');

  click('.navbar-guest-nav button.btn-default');
  fillIn('#appModal .form-group:first-child input', 'SomeFake');
  fillIn('#appModal .form-group:last-child input', 'pass1234');
  click('#appModal .btn-primary');

  andThen(function() {
    assert.equal(getToastMessage(), 'Unknown error has occured.');
  });
});

test('app went away', function(assert) {
  assert.expect(1);

  Ember.$.mockjax({
    url: '/api/auth/',
    status: 0
  });

  visit('/');

  click('.navbar-guest-nav button.btn-default');
  fillIn('#appModal .form-group:first-child input', 'SomeFake');
  fillIn('#appModal .form-group:last-child input', 'pass1234');
  click('#appModal .btn-primary');

  andThen(function() {
    assert.equal(getToastMessage(), 'Lost connection with application.');
  });
});

test('not found', function(assert) {
  assert.expect(1);

  Ember.$.mockjax({
    url: '/api/auth/',
    status: 404,
    responseText: {
      'detail': 'Not found'
    }
  });

  visit('/');

  click('.navbar-guest-nav button.btn-default');
  fillIn('#appModal .form-group:first-child input', 'SomeFake');
  fillIn('#appModal .form-group:last-child input', 'pass1234');
  click('#appModal .btn-primary');

  andThen(function() {
    assert.equal(getToastMessage(), 'Action link is invalid.');
  });
});

test('permission denied', function(assert) {
  assert.expect(1);

  Ember.$.mockjax({
    url: '/api/auth/',
    status: 403,
    responseText: {
      'detail': 'Permission denied'
    }
  });

  visit('/');

  click('.navbar-guest-nav button.btn-default');
  fillIn('#appModal .form-group:first-child input', 'SomeFake');
  fillIn('#appModal .form-group:last-child input', 'pass1234');
  click('#appModal .btn-primary');

  andThen(function() {
    assert.equal(getToastMessage(), "You don't have permission to perform this action.");
  });
});

test('permission denied with reason', function(assert) {
  assert.expect(1);

  Ember.$.mockjax({
    url: '/api/auth/',
    status: 403,
    responseText: {
      'detail': 'Lorem ipsum dolor met.'
    }
  });

  visit('/');

  click('.navbar-guest-nav button.btn-default');
  fillIn('#appModal .form-group:first-child input', 'SomeFake');
  fillIn('#appModal .form-group:last-child input', 'pass1234');
  click('#appModal .btn-primary');

  andThen(function() {
    assert.equal(getToastMessage(), 'Lorem ipsum dolor met.');
  });
});
