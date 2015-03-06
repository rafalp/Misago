import Ember from 'ember';
import { module, test } from 'qunit';
import startApp from '../helpers/start-app';

var application;

module('Acceptance: ForgottenPassword', {
  beforeEach: function() {
    application = startApp();
  },

  afterEach: function() {
    Ember.run(application, 'destroy');
    Ember.$.mockjax.clear();
  }
});

test('visiting /forgotten-password', function(assert) {
  visit('/forgotten-password');

  andThen(function() {
    assert.equal(currentPath(), 'forgotten-password.index');
  });
});

test('request password change link without entering e-mail', function(assert) {
  visit('/forgotten-password');
  click('.forgotten-password-page form .btn-primary');

  andThen(function() {
    assert.equal(currentPath(), 'forgotten-password.index');

    var error = Ember.$.trim(find('.flash-message p').text());
    assert.equal(error, 'Enter e-mail address.');
  });
});

test('request password change link with invalid e-mail', function(assert) {
  var message = 'Entered e-mail is invalid.';
  Ember.$.mockjax({
    url: "/api/change-password/send-link/",
    status: 400,
    responseText: {
      'detail': message,
      'code': 'invalid_email'
    }
  });

  visit('/forgotten-password');
  fillIn('.forgotten-password-page form input', 'not-valid-email');
  click('.forgotten-password-page form .btn-primary');

  andThen(function() {
    assert.equal(currentPath(), 'forgotten-password.index');

    var error = Ember.$.trim(find('.flash-message p').text());
    assert.equal(error, message);
  });
});

test('request password change link with non-existing e-mail', function(assert) {
  var message = 'No user with this e-mail exists.';
  Ember.$.mockjax({
    url: "/api/change-password/send-link/",
    status: 400,
    responseText: {
      'detail': message,
      'code': 'not_found'
    }
  });

  visit('/forgotten-password');
  fillIn('.forgotten-password-page form input', 'not-valid-email');
  click('.forgotten-password-page form .btn-primary');

  andThen(function() {
    assert.equal(currentPath(), 'forgotten-password.index');

    var error = Ember.$.trim(find('.flash-message p').text());
    assert.equal(error, message);
  });
});

test('request password change link with user-activated account', function(assert) {
  var message = 'You have to activate your account before you will be able to sign in.';
  Ember.$.mockjax({
    url: "/api/change-password/send-link/",
    status: 400,
    responseText: {
      'detail': message,
      'code': 'inactive_user'
    }
  });

  visit('/forgotten-password');
  fillIn('.forgotten-password-page form input', 'valid@mail.com');
  click('.forgotten-password-page form .btn-primary');

  andThen(function() {
    assert.equal(currentPath(), 'forgotten-password.index');

    var error = Ember.$.trim(find('.flash-message p').text());
    assert.equal(error, message);
  });
});

test('request password change link with admin-activated account', function(assert) {
  var message = 'Your account has to be activated by Administrator before you will be able to sign in.';
  Ember.$.mockjax({
    url: "/api/change-password/send-link/",
    status: 400,
    responseText: {
      'detail': message,
      'code': 'inactive_admin'
    }
  });

  visit('/forgotten-password');
  fillIn('.forgotten-password-page form input', 'valid@mail.com');
  click('.forgotten-password-page form .btn-primary');

  andThen(function() {
    assert.equal(currentPath(), 'forgotten-password.index');

    var error = Ember.$.trim(find('.flash-message p').text());
    assert.equal(error, message);
  });
});

test('request password change link with banned account', function(assert) {
  var done = assert.async();
  Ember.$.mockjax({
    url: "/api/change-password/send-link/",
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

  visit('/forgotten-password');
  fillIn('.forgotten-password-page form input', 'valid@mail.com');
  click('.forgotten-password-page form .btn-primary');

  andThen(function() {
    var errorMessage = find('.lead p').text();
    assert.equal(errorMessage, 'You are banned for trolling.');

    var expirationMessage = find('.error-message>p').text();
    assert.equal(expirationMessage, 'This ban is permanent.');

    done();
  });
});

test('request password change link', function(assert) {
  var done = assert.async();
  Ember.$.mockjax({
    url: "/api/change-password/send-link/",
    status: 200,
    responseText: {
      'username': 'BobBoberson',
      'email': 'valid@mail.com'
    }
  });

  visit('/forgotten-password');
  fillIn('.forgotten-password-page form input', 'valid@mail.com');
  click('.forgotten-password-page form .btn-primary');

  andThen(function() {
    var pageHeader = Ember.$.trim(find('.page-header h1').text());
    assert.equal(pageHeader, 'Change password form link sent');

    done();
  });
});
