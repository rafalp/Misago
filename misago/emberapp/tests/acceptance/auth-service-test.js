import Ember from 'ember';
import { module, test } from 'qunit';
import startApp from '../helpers/start-app';
import createUser from '../helpers/create-user';

var application, container, session, service;

module('Acceptance: AuthService', {
  beforeEach: function() {
    application = startApp();
    container = application.__container__;
    session = container.lookup('store:local');
    service = container.lookup('service:auth');
  },
  afterEach: function() {
    Ember.run(application, 'destroy');
  }
});

test('anon user was logged in', function(assert) {
  assert.expect(2);

  var user = createUser();

  session.setItem('auth-user', user);
  service._handleAuthChange(true);

  assert.ok(service.get('needsSync'));
  assert.equal(service.get('syncToUser.username'), user.get('username'));
});

test('authenticated user was logged out', function(assert) {
  assert.expect(2);

  var user = createUser();

  service.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  service._handleAuthChange(false);
  assert.ok(service.get('needsSync'));
  assert.equal(service.get('syncToUser'), null);
});

test('authenticated user was re-logged', function(assert) {
  assert.expect(2);

  var user = createUser();
  var newUser = createUser({
    id: user.get('id') + 123,
    username: 'justKyle'
  });

  service.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  service._handleUserChange(newUser);

  assert.ok(service.get('needsSync'));
  assert.equal(service.get('syncToUser.username'), newUser.get('username'));
});

test('authenticated user was updated', function(assert) {
  assert.expect(2);

  var user = createUser();
  var newUser = createUser({
    username: 'justKyle'
  });

  service.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  service._handleUserChange(newUser);

  assert.ok(!service.get('needsSync'));
  assert.equal(service.get('user.username'), newUser.get('username'));
});
