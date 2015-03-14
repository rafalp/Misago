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

test('sets title correctly', function(assert) {
  assert.expect(2);

  var route = this.subject();

  route.set('settings', {
    'forum_index_title': '',
    'forum_name': 'Forum Name',
  });

  route.send('didTransition');
  assert.equal(document.title, 'Forum Name');

  route.set('settings', {
    'forum_index_title': 'Welcome to Forum!',
    'forum_name': 'Forum Name',
  });

  route.send('didTransition');
  assert.equal(document.title, 'Welcome to Forum!');
});
