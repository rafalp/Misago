import {
  moduleFor,
  test
} from 'ember-qunit';

moduleFor('component:guest-nav', 'GuestNavController');

test('it exists', function(assert) {
  assert.expect(1);

  var controller = this.subject();
  assert.ok(controller);
});
