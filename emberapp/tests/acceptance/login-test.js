import Ember from 'ember';
import { module, test } from 'qunit';
import startApp from '../helpers/start-app';
import destroyModal from '../helpers/destroy-modal';
import getToastMessage from '../helpers/toast-message';

var application;

module('Acceptance: Login', {
  beforeEach: function() {
    Ember.$('#hidden-login-form').on('submit.stopInTest', function(event) {
      event.stopPropagation();
      return false;
    });
    application = startApp();
  },

  afterEach: function() {
    Ember.$('#hidden-login-form').off('submit.stopInTest');
    destroyModal();
    Ember.run(application, 'destroy');
    Ember.$.mockjax.clear();
  }
});

test('login with empty credentials', function(assert) {
  assert.expect(1);

  visit('/');
  click('.navbar-guest-nav button.btn-sign-in');
  click('#appModal .btn-primary');

  andThen(function() {
    assert.equal(getToastMessage(), 'Fill out both fields.');
  });
});

test('backend errored', function(assert) {
  assert.expect(1);

  Ember.$.mockjax({
    url: '/api/auth/',
    status: 500
  });

  visit('/');

  click('.navbar-guest-nav .btn-sign-in');
  fillIn('#appModal .form-group:first-child input', 'SomeFake');
  fillIn('#appModal .form-group:last-child input', 'pass1234');
  click('#appModal .btn-primary');

  andThen(function() {
    assert.equal(getToastMessage(), 'Unknown error has occured.');
  });
});

test('login with invalid credentials', function(assert) {
  assert.expect(1);

  var message = 'Login or password is incorrect.';
  Ember.$.mockjax({
    url: '/api/auth/',
    status: 400,
    responseText: {
      'detail': message,
      'code': 'invalid_login'
    }
  });

  visit('/');

  click('.navbar-guest-nav .btn-sign-in');
  fillIn('#appModal .form-group:first-child input', 'SomeFake');
  fillIn('#appModal .form-group:last-child input', 'pass1234');
  click('#appModal .btn-primary');

  andThen(function() {
    assert.equal(getToastMessage(), message);
  });
});

test('login to user-activated account', function(assert) {
  assert.expect(1);

  var message = 'You have to activate your account before you will be able to sign in.';
  Ember.$.mockjax({
    url: '/api/auth/',
    status: 400,
    responseText: {
      'detail': message,
      'code': 'inactive_user'
    }
  });

  visit('/');

  click('.navbar-guest-nav .btn-sign-in');
  fillIn('#appModal .form-group:first-child input', 'SomeFake');
  fillIn('#appModal .form-group:last-child input', 'pass1234');
  click('#appModal .btn-primary');

  andThen(function() {
    assert.equal(getToastMessage(), message);
  });
});

test('login to admin-activated account', function(assert) {
  assert.expect(1);

  var message = 'Your account has to be activated by Administrator before you will be able to sign in.';
  Ember.$.mockjax({
    url: '/api/auth/',
    status: 400,
    responseText: {
      'detail': message,
      'code': 'inactive_admin'
    }
  });

  visit('/');

  click('.navbar-guest-nav .btn-sign-in');
  fillIn('#appModal .form-group:first-child input', 'SomeFake');
  fillIn('#appModal .form-group:last-child input', 'pass1234');
  click('#appModal .btn-primary');

  andThen(function() {
    assert.equal(getToastMessage(), message);
  });
});

test('login to banned account', function(assert) {
  assert.expect(3);

  Ember.$.mockjax({
    url: '/api/auth/',
    status: 400,
    responseText: {
      'detail': {
        'expires_on': null,
        'message': {
          'plain': 'You are banned for trolling.',
          'html': '<p>You are banned for trolling.</p>',
        }
      },
      'code': 'banned'
    }
  });

  visit('/');

  click('.navbar-guest-nav .btn-sign-in');
  fillIn('#appModal .form-group:first-child input', 'SomeFake');
  fillIn('#appModal .form-group:last-child input', 'pass1234');
  click('#appModal .btn-primary');

  andThen(function() {
    assert.equal(currentPath(), 'error-banned');

    var banMessage = find('.lead p').text();
    assert.equal(banMessage, 'You are banned for trolling.');

    var expirationMessage = Ember.$.trim(find('.error-message>p').text());
    assert.equal(expirationMessage, 'This ban is permanent.');
  });
});

test('login successfully', function(assert) {
  assert.expect(2);

  Ember.$.mockjax({
    url: '/api/auth/',
    status: 200,
    responseText: {
      'username': 'SomeFake'
    }
  });

  visit('/');

  click('.navbar-guest-nav .btn-sign-in');
  fillIn('#appModal .form-group:first-child input', 'SomeFake');
  fillIn('#appModal .form-group:last-child input', 'pass1234');
  click('#appModal .btn-primary');

  andThen(function() {
    assert.equal(Ember.$('#hidden-login-form input[name="username"]').val(), 'SomeFake');
    assert.equal(Ember.$('#hidden-login-form input[name="password"]').val(), 'pass1234');
  });
});
