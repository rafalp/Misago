import Ember from 'ember';
import { initialize } from 'misago/initializers/trailing-slash';

var container, application;

module('TrailingSlashInitializer', {
  setup: function() {
    Ember.run(function() {
      application = Ember.Application.create();
      container = application.__container__;
      application.deferReadiness();
    });
  }
});

test('it exists', function() {
  initialize(container, application);

  ok(container.has('location:trailing-history'));
});

