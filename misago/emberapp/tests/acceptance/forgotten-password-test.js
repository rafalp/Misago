import Ember from 'ember';
import { module, test } from 'qunit';
import startApp from '../helpers/start-app';

var application;

module('Acceptance: ForgottenPassword', {
  beforeEach: function() {
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
    url: '/api/change-password/send-link/',
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
    url: '/api/change-password/send-link/',
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
    url: '/api/change-password/send-link/',
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
    url: '/api/change-password/send-link/',
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
    url: '/api/change-password/send-link/',
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
    url: '/api/change-password/send-link/',
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

test('invalid token is handled', function(assert) {
  var message = 'Token was rejected.';
  Ember.$.mockjax({
    url: '/api/change-password/1/token/validate-token/',
    status: 404,
    responseText: {
      'detail': message
    }
  });

  visit('/forgotten-password/1/token/');

  andThen(function() {
    assert.equal(currentPath(), 'forgotten-password.index');

    var errorMessage = Ember.$.trim(find('.flash-message>p').text());
    assert.equal(errorMessage, message);
  });
});

test('permission denied is handled', function(assert) {
  var message = 'Token was rejected.';
  Ember.$.mockjax({
    url: '/api/change-password/1/token/validate-token/',
    status: 403,
    responseText: {
      'detail': message
    }
  });

  visit('/forgotten-password/1/token/');

  andThen(function() {
    assert.equal(currentPath(), 'error-403');

    var errorMessage = Ember.$.trim(find('.lead').text());
    assert.equal(errorMessage, message);
  });
});

test('token is validated', function(assert) {
  Ember.$.mockjax({
    url: '/api/change-password/1/token/validate-token/',
    status: 200,
    responseText: {
      'user_id': 1,
      'token': 'token',
      'change_password_url': '/api/change-password-url/'
    }
  });

  visit('/forgotten-password/1/token/');

  andThen(function() {
    assert.equal(currentPath(), 'forgotten-password.change-form');
  });
});

test('no new password is entered', function(assert) {
  Ember.$.mockjax({
    url: '/api/change-password/1/token/validate-token/',
    status: 200,
    responseText: {
      'user_id': 1,
      'token': 'token',
      'change_password_url': '/api/change-password-url/'
    }
  });

  visit('/forgotten-password/1/token/');
  click('.forgotten-password-page form .btn-primary');

  andThen(function() {
    assert.equal(currentPath(), 'forgotten-password.change-form');

    var error = Ember.$.trim(find('.flash-message p').text());
    assert.equal(error, 'Enter new password.');
  });
});

test('new password is invalid', function(assert) {
  Ember.$.mockjax({
    url: '/api/change-password/1/token/validate-token/',
    status: 200,
    responseText: {
      'user_id': 1,
      'token': 'token',
      'change_password_url': '/api/change-password-url/'
    }
  });

  var message = 'Entered password is not allowed.';
  Ember.$.mockjax({
    url: '/api/change-password-url/',
    status: 400,
    responseText: {
      'detail': message
    }
  });

  visit('/forgotten-password/1/token/');
  fillIn('.forgotten-password-page form .control-input input', 'newp4ssw0rd');
  click('.forgotten-password-page form .btn-primary');

  andThen(function() {
    assert.equal(currentPath(), 'forgotten-password.change-form');

    var error = Ember.$.trim(find('.flash-message p').text());
    assert.equal(error, message);
  });
});

test('new password is accepted', function(assert) {
  Ember.$.mockjax({
    url: '/api/change-password/1/token/validate-token/',
    status: 200,
    responseText: {
      'user_id': 1,
      'token': 'token',
      'change_password_url': '/api/change-password-url/'
    }
  });

  var message = 'lul';
  Ember.$.mockjax({
    url: '/api/change-password-url/',
    status: 200
  });

  visit('/forgotten-password/1/token/');
  fillIn('.forgotten-password-page form .control-input input', 'newp4ssw0rd');
  click('.forgotten-password-page form .btn-primary');

  andThen(function() {
    assert.equal(currentPath(), 'forgotten-password.change-form');
    assert.ok(find('#loginModal').hasClass('in'));

    var message = Ember.$.trim(find('.flash-message p').text());
    assert.equal(message, "Your password has been changed.");
  });
});
