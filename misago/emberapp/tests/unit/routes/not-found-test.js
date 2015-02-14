import {
  moduleFor,
  test
} from 'ember-qunit';

moduleFor('route:not-found', 'NotFoundRoute');

test('it exists', function(assert) {
  var route = this.subject();
  assert.ok(route);
});
