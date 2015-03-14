import Ember from 'ember';
import { initialize } from '../../../initializers/django-location';
import { module, test } from 'qunit';

var container, application;

module('DjangoLocationInitializer', {
  beforeEach: function() {
    Ember.run(function() {
      application = Ember.Application.create();
      container = application.__container__;
      application.deferReadiness();
    });
  }
});

test('initializer registers location api', function(assert) {
  assert.expect(1);

  initialize(container, application);

  assert.ok(container.has('location:django-location'));
});

