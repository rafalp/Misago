import {
  moduleFor,
  test
} from 'ember-qunit';

moduleFor('service:clock');

test('it exists', function(assert) {
  assert.expect(1);

  var service = this.subject();
  assert.ok(service);
});
