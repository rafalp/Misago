import Ember from 'ember';
import { initialize } from '../../../initializers/auth-service';
import { module, test } from 'qunit';

var container, application;

module('AuthServiceInitializer', {
  beforeEach: function() {
    Ember.run(function() {
      application = Ember.Application.create();
      container = application.__container__;
      application.deferReadiness();
    });
  }
});

test('initializer registered auth and user', function(assert) {
  assert.expect(1);

  initialize(container, application);

  assert.ok(container.lookup('service:auth'));
});
