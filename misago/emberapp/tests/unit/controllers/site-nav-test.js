import {
  moduleFor,
  test
} from 'ember-qunit';

moduleFor('controller:site-nav', 'SiteNavController');

test('it exists', function(assert) {
  assert.expect(1);

  var controller = this.subject();
  assert.ok(controller);
});
