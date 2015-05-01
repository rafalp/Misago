import Ember from 'ember';
import { module, test } from 'qunit';
import startApp from '../helpers/start-app';
import getToastMessage from '../helpers/toast-message';

var application;

module('Acceptance: Account Activation', {
  beforeEach: function() {
    application = startApp();
  },

  afterEach: function() {
    Ember.$('#hidden-login-form').off('submit.stopInTest');
    Ember.$('#appModal').off();
    Ember.$('body').removeClass('modal-open');
    Ember.run(application, 'destroy');
    Ember.$.mockjax.clear();
  }
});

test('visiting /activation', function(assert) {
  assert.expect(1);

  visit('/activation');

  andThen(function() {
    assert.equal(currentPath(), 'activation.index');
  });
});

test('request activation link without entering e-mail', function(assert) {
  assert.expect(2);

  visit('/activation');
  click('.activation-page form .btn-primary');

  andThen(function() {
    assert.equal(currentPath(), 'activation.index');
    assert.equal(getToastMessage(), 'Enter e-mail address.');
  });
});

test('request activation link with invalid e-mail', function(assert) {
  assert.expect(2);

  var message = 'Entered e-mail is invalid.';
  Ember.$.mockjax({
    url: '/api/auth/send-activation/',
    status: 400,
    responseText: {
      'detail': message,
      'code': 'invalid_email'
    }
  });

  visit('/activation');
  fillIn('.activation-page form input', 'not-valid-email');
  click('.activation-page form .btn-primary');

  andThen(function() {
    assert.equal(currentPath(), 'activation.index');
    assert.equal(getToastMessage(), message);
  });
});

test('request activation link with non-existing e-mail', function(assert) {
  assert.expect(2);

  var message = 'No user with this e-mail exists.';
  Ember.$.mockjax({
    url: '/api/auth/send-activation/',
    status: 400,
    responseText: {
      'detail': message,
      'code': 'not_found'
    }
  });

  visit('/activation');
  fillIn('.activation-page form input', 'not-valid-email');
  click('.activation-page form .btn-primary');

  andThen(function() {
    assert.equal(currentPath(), 'activation.index');
    assert.equal(getToastMessage(), message);
  });
});

test('request activation link with user-activated account', function(assert) {
  assert.expect(2);

  var message = 'You have to activate your account before you will be able to sign in.';
  Ember.$.mockjax({
    url: '/api/auth/send-activation/',
    status: 400,
    responseText: {
      'detail': message,
      'code': 'inactive_user'
    }
  });

  visit('/activation');
  fillIn('.activation-page form input', 'valid@mail.com');
  click('.activation-page form .btn-primary');

  andThen(function() {
    assert.equal(currentPath(), 'activation.index');
    assert.equal(getToastMessage(), message);
  });
});

test('request activation link with admin-activated account', function(assert) {
  assert.expect(2);

  var message = 'Your account has to be activated by Administrator before you will be able to sign in.';
  Ember.$.mockjax({
    url: '/api/auth/send-activation/',
    status: 400,
    responseText: {
      'detail': message,
      'code': 'inactive_admin'
    }
  });

  visit('/activation');
  fillIn('.activation-page form input', 'valid@mail.com');
  click('.activation-page form .btn-primary');

  andThen(function() {
    assert.equal(currentPath(), 'activation.index');
    assert.equal(getToastMessage(), message);
  });
});

test('request activation link with banned account', function(assert) {
  assert.expect(2);

  Ember.$.mockjax({
    url: '/api/auth/send-activation/',
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

  visit('/activation');
  fillIn('.activation-page form input', 'valid@mail.com');
  click('.activation-page form .btn-primary');

  andThen(function() {
    var errorMessage = find('.lead p').text();
    assert.equal(errorMessage, 'You are banned for trolling.');

    var expirationMessage = Ember.$.trim(find('.error-message>p').text());
    assert.equal(expirationMessage, 'This ban is permanent.');
  });
});

test('request activation link', function(assert) {
  assert.expect(1);

  Ember.$.mockjax({
    url: '/api/auth/send-activation/',
    status: 200,
    responseText: {
      'username': 'BobBoberson',
      'email': 'valid@mail.com'
    }
  });

  visit('/activation');
  fillIn('.activation-page form input', 'valid@mail.com');
  click('.activation-page form .btn-primary');

  andThen(function() {
    var pageHeader = Ember.$.trim(find('.page-header h1').text());
    assert.equal(pageHeader, 'Activation link sent');
  });
});

test('invalid token is handled', function(assert) {
  assert.expect(2);

  var message = 'Token was rejected.';
  Ember.$.mockjax({
    url: '/api/auth/activate-account/1/token/',
    status: 400,
    responseText: {
      'detail': message
    }
  });

  visit('/activation/1/token/');

  andThen(function() {
    assert.equal(currentPath(), 'activation.index');
    assert.equal(getToastMessage(), message);
  });
});

test('permission denied is handled', function(assert) {
  assert.expect(2);

  var message = 'Token was rejected.';
  Ember.$.mockjax({
    url: '/api/auth/activate-account/1/token/',
    status: 403,
    responseText: {
      'detail': message
    }
  });

  visit('/activation/1/token/');

  andThen(function() {
    assert.equal(currentPath(), 'error-403');

    var errorMessage = Ember.$.trim(find('.lead').text());
    assert.equal(errorMessage, message);
  });
});

test('account is activated', function(assert) {
  assert.expect(2);

  var message = 'Yur account has been activated!';
  Ember.$.mockjax({
    url: '/api/auth/activate-account/1/token/',
    status: 200,
    responseText: {
      'detail': message
    }
  });

  visit('/activation/1/token/');

  andThen(function() {
    assert.equal(currentPath(), 'index');
    assert.equal(getToastMessage(), message);
  });
});
