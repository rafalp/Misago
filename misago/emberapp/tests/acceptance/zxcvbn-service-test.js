/* global zxcvbn */
import Ember from 'ember';
import { module, test } from 'qunit';
import startApp from '../helpers/start-app';

var application, container, service;

module('Acceptance: ZxcvbnService', {
  beforeEach: function() {
    application = startApp();
    container = application.__container__;
    service = container.lookup('service:zxcvbn');
  },
  afterEach: function() {
    Ember.run(application, 'destroy');
  }
});

test('loading zxcvbn and testing password with it', function(assert) {
  var done = assert.async();
  assert.expect(2);

  Ember.run(function() {
    service.loadLibrary().then(function() {
      assert.ok(typeof zxcvbn !== 'undefined');
      assert.ok(service.scorePassword('L0r3m !p5um') > 0);
        done();
    });
  });
});
