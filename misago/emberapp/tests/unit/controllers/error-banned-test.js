import {
  moduleFor,
  test
} from 'ember-qunit';

moduleFor('controller:error-banned', 'ErrorBannedController');

test('it exists', function(assert) {
  assert.expect(1);

  var controller = this.subject();
  assert.ok(controller);
});

test('isPermanent works', function(assert) {
  assert.expect(2);

  var controller = this.subject();

  controller.set('model', {'expires_on': null});
  assert.ok(controller.get('isPermanent'));

  controller.set('model', {'expires_on': 'nope'});
  assert.ok(!controller.get('isPermanent'));
});

test('expiresMoment works', function(assert) {
  assert.expect(2);

  var controller = this.subject();

  controller.set('model', {'expires_on': null});
  assert.equal(controller.get('expiresMoment'), null);

  controller.set('model', {'expires_on': '2015-07-30T12:15:00Z'});
  assert.ok(controller.get('expiresMoment').fromNow);
});

test('expiresOn works', function(assert) {
  assert.expect(2);

  var controller = this.subject();

  controller.set('model', {'expires_on': null});
  assert.equal(controller.get('expiresOn'), null);

  controller.set('model', {'expires_on': '2015-07-30T12:15:00Z'});
  assert.ok(controller.get('expiresOn').fromNow);
});

test('isExpired works', function(assert) {
  assert.expect(3);

  var controller = this.subject();

  controller.set('model', {'expires_on': null});
  assert.ok(!controller.get('isExpired'));

  controller.set('model', {'expires_on': '2014-07-30T12:15:00Z'});
  assert.ok(controller.get('isExpired'));

  controller.set('model', {'expires_on': '2026-07-30T12:15:00Z'});
  assert.ok(!controller.get('isExpired'));
});
