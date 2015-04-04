import {
  moduleFor,
  test
} from 'ember-qunit';

moduleFor('component:ban-expires', 'BanExpiresComponent');

test('it exists', function(assert) {
  assert.expect(1);

  var component = this.subject();
  assert.ok(component);
});

test('isPermanent works', function(assert) {
  assert.expect(2);

  var component = this.subject();

  component.set('model', {'expires_on': null});
  assert.ok(component.get('isPermanent'));

  component.set('model', {'expires_on': 'nope'});
  assert.ok(!component.get('isPermanent'));
});

test('expiresMoment works', function(assert) {
  assert.expect(2);

  var component = this.subject();

  component.set('model', {'expires_on': null});
  assert.equal(component.get('expiresMoment'), null);

  component.set('model', {'expires_on': '2015-07-30T12:15:00Z'});
  assert.ok(component.get('expiresMoment').fromNow);
});

test('expiresOn works', function(assert) {
  assert.expect(2);

  var component = this.subject();

  component.set('model', {'expires_on': null});
  assert.equal(component.get('expiresOn'), null);

  component.set('model', {'expires_on': '2015-07-30T12:15:00Z'});
  assert.ok(component.get('expiresOn').fromNow);
});

test('isExpired works', function(assert) {
  assert.expect(3);

  var component = this.subject();

  component.set('model', {'expires_on': null});
  assert.ok(!component.get('isExpired'));

  component.set('model', {'expires_on': '2014-07-30T12:15:00Z'});
  assert.ok(component.get('isExpired'));

  component.set('model', {'expires_on': '2026-07-30T12:15:00Z'});
  assert.ok(!component.get('isExpired'));
});
