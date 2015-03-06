import Ember from 'ember';
import { module, test } from 'qunit';
import startApp from '../helpers/start-app';

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
    Ember.$('#loginModal').off();
    Ember.$('body').removeClass('modal-open');
    Ember.run(application, 'destroy');
    Ember.$.mockjax.clear();
  }
});

test('login with empty credentials', function(assert) {
  visit('/');
  click('.guest-nav button.btn-login');
  click('#loginModal .btn-primary');

  andThen(function() {
    var error = Ember.$.trim(find('.flash-message p').text());
    assert.equal(error, 'Fill out both fields.');
  });
});

test('login with invalid credentials', function(assert) {
  var message = 'Login or password is incorrect.';
  Ember.$.mockjax({
    url: "/api/auth/login/",
    status: 400,
    responseText: {
      'detail': message,
      'code': 'invalid_login'
    }
  });

  visit('/');

  click('.guest-nav .btn-login');
  fillIn('#loginModal .form-group:first-child input', 'SomeFake');
  fillIn('#loginModal .form-group:last-child input', 'pass1234');
  click('#loginModal .btn-primary');

  andThen(function() {
    var error = Ember.$.trim(find('.flash-message p').text());
    assert.equal(error, message);
  });
});

test('login to user-activated account', function(assert) {
  var message = 'You have to activate your account before you will be able to sign in.';
  Ember.$.mockjax({
    url: "/api/auth/login/",
    status: 400,
    responseText: {
      'detail': message,
      'code': 'inactive_user'
    }
  });

  visit('/');

  click('.guest-nav .btn-login');
  fillIn('#loginModal .form-group:first-child input', 'SomeFake');
  fillIn('#loginModal .form-group:last-child input', 'pass1234');
  click('#loginModal .btn-primary');

  andThen(function() {
    var error = Ember.$.trim(find('.flash-message p').text());
    assert.equal(error, message);
  });
});

test('login to admin-activated account', function(assert) {
  var message = 'Your account has to be activated by Administrator before you will be able to sign in.';
  Ember.$.mockjax({
    url: "/api/auth/login/",
    status: 400,
    responseText: {
      'detail': message,
      'code': 'inactive_admin'
    }
  });

  visit('/');

  click('.guest-nav .btn-login');
  fillIn('#loginModal .form-group:first-child input', 'SomeFake');
  fillIn('#loginModal .form-group:last-child input', 'pass1234');
  click('#loginModal .btn-primary');

  andThen(function() {
    var error = Ember.$.trim(find('.flash-message p').text());
    assert.equal(error, message);
  });
});

test('login to banned account', function(assert) {
  var done = assert.async();
  Ember.$.mockjax({
    url: "/api/auth/login/",
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

  click('.guest-nav .btn-login');
  fillIn('#loginModal .form-group:first-child input', 'SomeFake');
  fillIn('#loginModal .form-group:last-child input', 'pass1234');
  click('#loginModal .btn-primary');

  andThen(function() {
    var errorMessage = find('.lead p').text();
    assert.equal(errorMessage, 'You are banned for trolling.');

    var expirationMessage = find('.error-message>p').text();
    assert.equal(expirationMessage, 'This ban is permanent.');

    done();
  });
});

test('login successfully', function(assert) {
  Ember.$.mockjax({
    url: "/api/auth/login/",
    status: 200,
    responseText: {
      'username': 'SomeFake'
    }
  });

  visit('/');

  click('.guest-nav .btn-login');
  fillIn('#loginModal .form-group:first-child input', 'SomeFake');
  fillIn('#loginModal .form-group:last-child input', 'pass1234');
  click('#loginModal .btn-primary');

  andThen(function() {
    assert.equal(Ember.$('#hidden-login-form input[name="username"]').val(), 'SomeFake');
    assert.equal(Ember.$('#hidden-login-form input[name="password"]').val(), 'pass1234');
  });
});
