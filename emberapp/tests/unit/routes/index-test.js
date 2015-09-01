import {
  moduleFor,
  test
} from 'ember-qunit';

var document_title = document.title;

moduleFor('route:index', 'IndexRoute', {
  afterEach: function() {
    document.title = document_title;
  }
});

test('it exists', function(assert) {
  assert.expect(1);

  var route = this.subject();
  assert.ok(route);
});
