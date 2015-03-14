import {
  moduleFor,
  test
} from 'ember-qunit';

moduleFor('controller:forgotten-password/request-link', 'RequestLinkController');

test('it exists', function(assert) {
  assert.expect(1);

  var controller = this.subject();
  assert.ok(controller);
});
