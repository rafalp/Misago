import Ember from 'ember';
import { module, test } from 'qunit';
import startApp from '../helpers/start-app';
import destroyModal from '../helpers/destroy-modal';
import getToastMessage from '../helpers/toast-message';

var application;

module('Acceptance: Register', {
  beforeEach: function() {
    application = startApp();
  },

  afterEach: function() {
    window.MisagoData['misagoSettings']['account_activation'] = 'none';
    destroyModal();
    Ember.run(application, 'destroy');
    Ember.$.mockjax.clear();
  }
});

test('registration is closed', function(assert) {
  window.MisagoData['misagoSettings']['account_activation'] = 'closed';
  assert.expect(1);

  visit('/');
  click('.navbar-guest-nav button.btn-success');

  andThen(function() {
    assert.equal(Ember.$.trim(find('.modal-register-closed .lead').text()), 'New registrations are currently not being accepted.');
  });
});

test('register with empty credentials', function(assert) {
  assert.expect(1);

  visit('/');
  click('.navbar-guest-nav button.btn-success');
  click('#appModal .btn-primary');

  andThen(function() {
    assert.equal(getToastMessage(), 'Form contains errors.');
  });
});

test('register with invalid credentials', function(assert) {
  assert.expect(1);

  visit('/');
  click('.navbar-guest-nav button.btn-success');
  fillIn('#appModal #id_username', 'a');
  fillIn('#appModal #id_password', 'b');
  fillIn('#appModal #id_email', 'c');
  click('#appModal .btn-primary');

  andThen(function() {
    assert.equal(getToastMessage(), 'Form contains errors.');
  });
});

test('register with rejected credentials', function(assert) {
  assert.expect(1);

  Ember.$.mockjax({
    url: "/api/users/",
    status: 400
  });

  visit('/');
  click('.navbar-guest-nav button.btn-success');
  fillIn('#appModal #id_username', 'Lorem');
  fillIn('#appModal #id_password', 'ipsum123');
  fillIn('#appModal #id_email', 'lorem@ipsum.com');
  click('#appModal .btn-primary');

  andThen(function() {
    assert.equal(getToastMessage(), 'Form contains errors.');
  });
});

test('register banned', function(assert) {
  assert.expect(3);

  Ember.$.mockjax({
    url: "/api/users/",
    status: 403,
    responseText: {
      'detail': 'Thy are banned!',
      'ban': {
        'expires_on': null,
        'message': {
          'plain': 'You are banned for trolling.',
          'html': '<p>You are banned for trolling.</p>',
        }
      }
    }
  });

  visit('/');
  click('.navbar-guest-nav button.btn-success');
  fillIn('#appModal #id_username', 'Lorem');
  fillIn('#appModal #id_password', 'ipsum123');
  fillIn('#appModal #id_email', 'lorem@ipsum.com');
  click('#appModal .btn-primary');

  andThen(function() {
    assert.equal(currentPath(), 'error-banned');

    var banMessage = find('.lead p').text();
    assert.equal(banMessage, 'You are banned for trolling.');

    var expirationMessage = Ember.$.trim(find('.error-message>p').text());
    assert.equal(expirationMessage, 'This ban is permanent.');
  });
});

test('register active user', function(assert) {
  assert.expect(1);

  Ember.$.mockjax({
    url: "/api/users/",
    status: 200,
    responseText: {
      'activation': 'active',
      'username': 'BobBoberson',
      'email': 'bob@weebl.com'
    }
  });

  visit('/');
  click('.navbar-guest-nav button.btn-success');
  fillIn('#appModal #id_username', 'Lorem');
  fillIn('#appModal #id_password', 'ipsum123');
  fillIn('#appModal #id_email', 'lorem@ipsum.com');
  click('#appModal .btn-primary');

  andThen(function() {
    var expectedMessage = 'BobBoberson, your account has been registered successfully.';
    assert.equal(Ember.$.trim(find('.modal-register-done .lead').text()), expectedMessage);
  });
});

test('register admin-activated user', function(assert) {
  assert.expect(1);

  Ember.$.mockjax({
    url: "/api/users/",
    status: 200,
    responseText: {
      'activation': 'activation_by_admin',
      'username': 'BobBoberson',
      'email': 'bob@weebl.com'
    }
  });

  visit('/');
  click('.navbar-guest-nav button.btn-success');
  fillIn('#appModal #id_username', 'Lorem');
  fillIn('#appModal #id_password', 'ipsum123');
  fillIn('#appModal #id_email', 'lorem@ipsum.com');
  click('#appModal .btn-primary');

  andThen(function() {
    var expectedMessage = 'BobBoberson, your account has been registered successfully, but site administrator has to activate it before you will be able to sing in.';
    assert.equal(Ember.$.trim(find('.modal-register-done .lead').text()), expectedMessage);
  });
});

test('register self-activated user', function(assert) {
  assert.expect(1);

  Ember.$.mockjax({
    url: "/api/users/",
    status: 200,
    responseText: {
      'activation': 'activation_by_user',
      'username': 'BobBoberson',
      'email': 'bob@weebl.com'
    }
  });

  visit('/');
  click('.navbar-guest-nav button.btn-success');
  fillIn('#appModal #id_username', 'Lorem');
  fillIn('#appModal #id_password', 'ipsum123');
  fillIn('#appModal #id_email', 'lorem@ipsum.com');
  click('#appModal .btn-primary');

  andThen(function() {
    var expectedMessage = 'BobBoberson, your account has been registered successfully, but you have to activate it before you will be able to sign in.';
    assert.equal(Ember.$.trim(find('.modal-register-done .lead').text()), expectedMessage);
  });
});

