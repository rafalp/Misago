import Ember from 'ember';
import { module, test } from 'qunit';
import startApp from '../helpers/start-app';
import destroyModal from '../helpers/destroy-modal';
import getToastMessage from '../helpers/toast-message';

var application;

module('Acceptance: Forgotten Password Change', {
  beforeEach: function() {
    application = startApp();
  },
  afterEach: function() {
    destroyModal();
    Ember.run(application, 'destroy');
    Ember.$.mockjax.clear();
  }
});

test('visiting /forgotten-password', function(assert) {
  assert.expect(1);

  visit('/forgotten-password');

  andThen(function() {
    assert.equal(currentPath(), 'forgotten-password.index');
  });
});

test('request password change link without entering e-mail', function(assert) {
  assert.expect(2);

  visit('/forgotten-password');
  click('.forgotten-password-page form .btn-primary');

  andThen(function() {
    assert.equal(currentPath(), 'forgotten-password.index');
    assert.equal(getToastMessage(), 'Enter e-mail address.');
  });
});

test('request password change link with invalid e-mail', function(assert) {
  assert.expect(2);

  var message = 'Entered e-mail is invalid.';
  Ember.$.mockjax({
    url: '/api/auth/send-password-form/',
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
    assert.equal(getToastMessage(), message);
  });
});

test('request password change link with non-existing e-mail', function(assert) {
  assert.expect(2);

  var message = 'No user with this e-mail exists.';
  Ember.$.mockjax({
    url: '/api/auth/send-password-form/',
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
    assert.equal(getToastMessage(), message);
  });
});

test('request password change link with user-activated account', function(assert) {
  assert.expect(2);

  var message = 'You have to activate your account before you will be able to sign in.';
  Ember.$.mockjax({
    url: '/api/auth/send-password-form/',
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
    assert.equal(getToastMessage(), message);
  });
});

test('request password change link with admin-activated account', function(assert) {
  assert.expect(2);

  var message = 'Your account has to be activated by Administrator before you will be able to sign in.';
  Ember.$.mockjax({
    url: '/api/auth/send-password-form/',
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
    assert.equal(getToastMessage(), message);
  });
});

test('request password change link with banned account', function(assert) {
  assert.expect(2);

  Ember.$.mockjax({
    url: '/api/auth/send-password-form/',
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

    var expirationMessage = Ember.$.trim(find('.error-message>p').text());
    assert.equal(expirationMessage, 'This ban is permanent.');
  });
});

test('request password change link', function(assert) {
  assert.expect(1);

  Ember.$.mockjax({
    url: '/api/auth/send-password-form/',
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
  });
});

test('invalid token is handled', function(assert) {
  assert.expect(2);

  var message = 'Token was rejected.';
  Ember.$.mockjax({
    url: '/api/auth/change-password/1/token/',
    status: 400,
    responseText: {
      'detail': message
    }
  });

  visit('/forgotten-password/1/token/');

  andThen(function() {
    assert.equal(currentPath(), 'forgotten-password.index');
    assert.equal(getToastMessage(), message);
  });
});

test('permission denied is handled', function(assert) {
  assert.expect(2);

  var message = 'Token was rejected.';
  Ember.$.mockjax({
    url: '/api/auth/change-password/1/token/',
    status: 403,
    responseText: {
      'detail': message
    }
  });

  visit('/forgotten-password/1/token/');

  andThen(function() {
    assert.equal(currentPath(), 'error-403');

    var errorMessage = Ember.$.trim(find('.error-page .lead').text());
    assert.equal(errorMessage, message);
  });
});

test('token is validated', function(assert) {
  assert.expect(1);

  Ember.$.mockjax({
    url: '/api/auth/change-password/1/token/',
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
  assert.expect(2);

  Ember.$.mockjax({
    url: '/api/auth/change-password/1/token/',
    status: 200,
    responseText: {
      'user_id': 1,
      'token': 'token'
    }
  });

  visit('/forgotten-password/1/token/');
  click('.forgotten-password-page form .btn-primary');

  andThen(function() {
    assert.equal(currentPath(), 'forgotten-password.change-form');
    assert.equal(getToastMessage(), 'Enter new password.');
  });
});

test('new password is invalid', function(assert) {
  assert.expect(2);

  Ember.$.mockjax({
    url: '/api/auth/change-password/1/token/',
    type: 'GET',
    status: 200,
    responseText: {
      'user_id': 1,
      'token': 'token'
    }
  });

  var message = 'Entered password is not allowed.';
  Ember.$.mockjax({
    url: '/api/auth/change-password/1/token/',
    type: 'POST',
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
    assert.equal(getToastMessage(), message);
  });
});

test('new password is accepted', function(assert) {
  assert.expect(3);

  Ember.$.mockjax({
    url: '/api/auth/change-password/1/token/',
    type: 'GET',
    status: 200,
    responseText: {
      'user_id': 1,
      'token': 'token'
    }
  });

  Ember.$.mockjax({
    url: '/api/auth/change-password/1/token/',
    type: 'POST',
    status: 200,
    responseText: {'detail': 'ok'}
  });

  visit('/forgotten-password/1/token/');
  fillIn('.forgotten-password-page form .control-input input', 'newp4ssw0rd');
  click('.forgotten-password-page form .btn-primary');

  andThen(function() {
    assert.equal(currentPath(), 'forgotten-password.change-form');
    assert.equal(getToastMessage(), "Your password has been changed.");
    assert.ok(find('#appModal').hasClass('in'));
  });
});
