import Ember from 'ember';
import { module, test } from 'qunit';
import startApp from '../helpers/start-app';

var application, container, service;

module('Acceptance: Auth denyAuthenticated and denyAnonymous tests', {
  beforeEach: function() {
    application = startApp();
    container = application.__container__;
    service = container.lookup('service:auth');
  },

  afterEach: function() {
    Ember.run(application, 'destroy');
  }
});

test('guest can access protected route', function(assert) {
  assert.expect(1);

  visit('/forgotten-password');

  andThen(function() {
    assert.equal(currentPath(), 'forgotten-password.index');
  });
});

test('authenticated is denied access to protected route', function(assert) {
  assert.expect(2);

  service.set('isAuthenticated', true);

  visit('/forgotten-password');

  andThen(function() {
    assert.equal(currentPath(), 'error-403');

    var errorMessage = Ember.$.trim(find('.error-message .lead').text());
    assert.equal(errorMessage, 'Only guests can change forgotten password.');
  });
});
