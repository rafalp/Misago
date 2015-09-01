import {
  moduleFor,
  test
} from 'ember-qunit';

moduleFor('route:forgotten-password/index');

test('it exists', function(assert) {
  assert.expect(1);

  var route = this.subject();
  assert.ok(route);
});
