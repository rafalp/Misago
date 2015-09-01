import {
  moduleForModel,
  test
} from 'ember-qunit';

moduleForModel('legal-page', 'LegalPage');

test('it exists', function(assert) {
  assert.expect(1);

  var model = this.subject();
  assert.ok(!!model);
});
