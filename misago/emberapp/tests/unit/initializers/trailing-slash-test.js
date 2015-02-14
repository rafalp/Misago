import Ember from 'ember';
import { initialize } from 'misago/initializers/trailing-slash';
import { module, test } from 'qunit';

var container, application;

module('TrailingSlashInitializer', {
  beforeEach: function() {
    Ember.run(function() {
      application = Ember.Application.create();
      container = application.__container__;
      application.deferReadiness();
    });
  }
});

test('it exists', function(assert) {
  initialize(container, application);

  assert.ok(container.has('location:trailing-history'));
});

