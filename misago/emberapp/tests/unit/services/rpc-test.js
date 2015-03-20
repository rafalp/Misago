import {
  moduleFor,
  test
} from 'ember-qunit';

moduleFor('service:rpc');

test('unpluralizeUrlProcedure fixes urls', function(assert) {
  assert.expect(2);

  var service = this.subject();

  var url = service.unpluralizeUrlProcedure('/some-words/', 'some-word');
  assert.equal(url, '/some-word/');

  url = service.unpluralizeUrlProcedure('/model/some-words/', 'some-word');
  assert.equal(url, '/model/some-word/');
});
