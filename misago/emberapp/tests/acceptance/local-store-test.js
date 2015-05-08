import Ember from 'ember';
import { module, test } from 'qunit';
import startApp from '../helpers/start-app';

var application, container, service;

module('Acceptance: LocalStore', {
  beforeEach: function() {
    application = startApp();
    container = application.__container__;
    service = container.lookup('store:local');
  },
  afterEach: function() {
    Ember.run(application, 'destroy');
  }
});

test('getItem and setItem', function(assert) {
  assert.expect(2);

  assert.equal(service.getItem('undefinedKey'), null);

  var testKey = 'definedKey';
  var testValue = 'definedValue';

  service.setItem(testKey, testValue);
  assert.equal(service.getItem(testKey), testValue);
});

test('registered watcher is fired', function(assert) {
  var done = assert.async();
  assert.expect(1);

  var testKey = 'watchedKey';
  var testValue = 'watchedValue';

  service.watchItem(testKey, function(newValue) {
    assert.equal(testValue, newValue);
    done();
  });

  service._handleStorageEvent({key: 'unwatchedKey'});
  service._handleStorageEvent({
    key: service.prefixKey(testKey),
    newValue: testValue
  });
});
