/* global zxcvbn */
import Ember from 'ember';
import { module, test } from 'qunit';
import startApp from '../helpers/start-app';

var application, container, service;

module('Acceptance: CropitService', {
  beforeEach: function() {
    application = startApp();
    container = application.__container__;
    service = container.lookup('service:cropit');
  },
  afterEach: function() {
    Ember.run(application, 'destroy');
  }
});

test('loading cropit jquery extension', function(assert) {
  var done = assert.async();
  assert.expect(1);

  Ember.run(function() {
    service.load().then(function() {
      assert.ok(typeof Ember.$.fn.cropit !== 'undefined');
      done();
    });
  });
});
