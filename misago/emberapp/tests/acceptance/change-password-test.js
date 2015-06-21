import Ember from 'ember';
import { module, test } from 'qunit';
import startApp from '../helpers/start-app';
import getToastMessage from '../helpers/toast-message';
import createUser from '../helpers/create-user';

var application, container, auth;

module('Acceptance: Change Password', {
  beforeEach: function() {
    application = startApp();
    container = application.__container__;
    auth = container.lookup('service:auth');
  },
  afterEach: function() {
    Ember.run(application, 'destroy');
    Ember.$.mockjax.clear();
  }
});

test('/options/change-password form can be accessed', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  assert.expect(1);

  visit('/options/change-password/');

  andThen(function() {
    assert.equal(currentPath(), 'options.password.index');
  });
});

test('/options/change-password form handles empty submission', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  assert.expect(5);

  visit('/options/change-password/');
  click('.panel-form .panel-footer .btn-primary');

  andThen(function() {
    assert.equal(currentPath(), 'options.password.index');
    assert.equal(getToastMessage(), 'Form contains errors.');

    var newPasswordValidation = Ember.$('#id_new_password').parents('.form-group').find('.help-block.errors');
    assert.equal(Ember.$.trim(newPasswordValidation.text()), 'Enter new password.');

    var repeatPasswordValidation = Ember.$('#id_repeat_password').parents('.form-group').find('.help-block.errors');
    assert.equal(Ember.$.trim(repeatPasswordValidation.text()), 'Repeat new password.');

    var passwordValidation = Ember.$('#id_password').parents('.form-group').find('.help-block.errors');
    assert.equal(Ember.$.trim(passwordValidation.text()), 'Enter current password.');
  });
});

test('/options/change-password form handles invalid submission', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  assert.expect(3);

  visit('/options/change-password/');
  fillIn('#id_new_password', 'not-valid-password');
  fillIn('#id_password', 'password');
  click('.panel-form .panel-footer .btn-primary');

  andThen(function() {
    assert.equal(currentPath(), 'options.password.index');
    assert.equal(getToastMessage(), 'Form contains errors.');

    var repeatPasswordValidation = Ember.$('#id_repeat_password').parents('.form-group').find('.help-block.errors');
    assert.equal(Ember.$.trim(repeatPasswordValidation.text()), 'Repeat new password.');
  });
});

test('/options/change-password form handles error 400', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  Ember.$.mockjax({
    url: "/api/users/" + user.get('id') + '/change-password/',
    status: 400,
    responseText: {
      'new_password': ['New password is bad.'],
      'password': ['Password is bad.']
    }
  });

  assert.expect(4);

  visit('/options/change-password/');
  fillIn('#id_new_password', 'V4lidPassword');
  fillIn('#id_repeat_password', 'V4lidPassword');
  fillIn('#id_password', 'password');
  click('.panel-form .panel-footer .btn-primary');

  andThen(function() {
    assert.equal(currentPath(), 'options.password.index');
    assert.equal(getToastMessage(), 'Form contains errors.');

    var newPasswordValidation = Ember.$('#id_new_password').parents('.form-group').find('.help-block.errors');
    assert.equal(Ember.$.trim(newPasswordValidation.text()), 'New password is bad.');

    var passwordValidation = Ember.$('#id_password').parents('.form-group').find('.help-block.errors');
    assert.equal(Ember.$.trim(passwordValidation.text()), 'Password is bad.');
  });
});

test('/options/change-password form handles valid submission', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  Ember.$.mockjax({
    url: "/api/users/" + user.get('id') + '/change-password/',
    status: 200,
    responseText: {
      'detail': 'Success happened!'
    }
  });

  assert.expect(2);

  visit('/options/change-password/');
  fillIn('#id_new_password', 'V4lidPassword');
  fillIn('#id_repeat_password', 'V4lidPassword');
  fillIn('#id_password', 'password');
  click('.panel-form .panel-footer .btn-primary');

  andThen(function() {
    assert.equal(currentPath(), 'options.password.index');
    assert.equal(getToastMessage(), 'Success happened!');
  });
});

test('/options/change-password/token handles invalid token', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  Ember.$.mockjax({
    url: "/api/users/" + user.get('id') + '/change-password/',
    status: 400,
    responseText: {
      'detail': 'Token is invalid.'
    }
  });

  assert.expect(2);

  visit('/options/change-password/token/');

  andThen(function() {
    assert.equal(currentPath(), 'options.password.index');
    assert.equal(getToastMessage(), 'Token is invalid.');
  });
});

test('/options/change-password/token handles valid token', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  Ember.$.mockjax({
    url: "/api/users/" + user.get('id') + '/change-password/',
    status: 200,
    responseText: {
      'detail': 'E-mail was changed.'
    }
  });

  assert.expect(2);

  visit('/options/change-password/token/');

  andThen(function() {
    assert.equal(currentPath(), 'options.password.index');
    assert.equal(getToastMessage(), 'E-mail was changed.');
  });
});

