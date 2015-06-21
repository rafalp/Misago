import Ember from 'ember';
import { module, test } from 'qunit';
import startApp from '../helpers/start-app';
import getToastMessage from '../helpers/toast-message';
import createUser from '../helpers/create-user';

var application, container, auth;

module('Acceptance: Change E-mail', {
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

test('/options/change-email form can be accessed', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  assert.expect(1);

  visit('/options/change-email/');

  andThen(function() {
    assert.equal(currentPath(), 'options.email.index');
  });
});

test('/options/change-email form handles empty submission', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  assert.expect(4);

  visit('/options/change-email/');
  click('.panel-form .panel-footer .btn-primary');

  andThen(function() {
    assert.equal(currentPath(), 'options.email.index');
    assert.equal(getToastMessage(), 'Form contains errors.');

    var emailValidation = Ember.$('#id_new_email').parents('.form-group').find('.help-block.errors');
    assert.equal(Ember.$.trim(emailValidation.text()), 'Enter new e-mail.');

    var passwordValidation = Ember.$('#id_password').parents('.form-group').find('.help-block.errors');
    assert.equal(Ember.$.trim(passwordValidation.text()), 'Enter current password.');
  });
});

test('/options/change-email form handles invalid submission', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  assert.expect(3);

  visit('/options/change-email/');
  fillIn('#id_new_email', 'not-valid-email');
  fillIn('#id_password', 'password');
  click('.panel-form .panel-footer .btn-primary');

  andThen(function() {
    assert.equal(currentPath(), 'options.email.index');
    assert.equal(getToastMessage(), 'Form contains errors.');

    var fieldValidation = Ember.$('#id_new_email').parents('.form-group').find('.help-block.errors');
    assert.equal(Ember.$.trim(fieldValidation.text()), 'Invalid e-mail address.');
  });
});

test('/options/change-email form handles error 400', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  Ember.$.mockjax({
    url: "/api/users/" + user.get('id') + '/change-email/',
    status: 400,
    responseText: {
      'new_email': ['E-mail is bad.'],
      'password': ['Password is bad.']
    }
  });

  assert.expect(4);

  visit('/options/change-email/');
  fillIn('#id_new_email', 'valid@email.com');
  fillIn('#id_password', 'password');
  click('.panel-form .panel-footer .btn-primary');

  andThen(function() {
    assert.equal(currentPath(), 'options.email.index');
    assert.equal(getToastMessage(), 'Form contains errors.');

    var emailValidation = Ember.$('#id_new_email').parents('.form-group').find('.help-block.errors');
    assert.equal(Ember.$.trim(emailValidation.text()), 'E-mail is bad.');

    var passwordValidation = Ember.$('#id_password').parents('.form-group').find('.help-block.errors');
    assert.equal(Ember.$.trim(passwordValidation.text()), 'Password is bad.');
  });
});

test('/options/change-email form handles valid submission', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  Ember.$.mockjax({
    url: "/api/users/" + user.get('id') + '/change-email/',
    status: 200,
    responseText: {
      'detail': 'Success happened!'
    }
  });

  assert.expect(2);

  visit('/options/change-email/');
  fillIn('#id_new_email', 'valid@email.com');
  fillIn('#id_password', 'password');
  click('.panel-form .panel-footer .btn-primary');

  andThen(function() {
    assert.equal(currentPath(), 'options.email.index');
    assert.equal(getToastMessage(), 'Success happened!');
  });
});

test('/options/change-email/token handles invalid token', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  Ember.$.mockjax({
    url: "/api/users/" + user.get('id') + '/change-email/',
    status: 400,
    responseText: {
      'detail': 'Token is invalid.'
    }
  });

  assert.expect(2);

  visit('/options/change-email/token/');

  andThen(function() {
    assert.equal(currentPath(), 'options.email.index');
    assert.equal(getToastMessage(), 'Token is invalid.');
  });
});

test('/options/change-email/token handles valid token', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  Ember.$.mockjax({
    url: "/api/users/" + user.get('id') + '/change-email/',
    status: 200,
    responseText: {
      'detail': 'E-mail was changed.'
    }
  });

  assert.expect(2);

  visit('/options/change-email/token/');

  andThen(function() {
    assert.equal(currentPath(), 'options.email.index');
    assert.equal(getToastMessage(), 'E-mail was changed.');
  });
});

