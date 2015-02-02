import {
  moduleFor,
  test
} from 'ember-qunit';

var document_title = document.title;

moduleFor('route:index', 'IndexRoute', {
  teardown: function() {
    document.title = document_title;
  }
});

test('it exists', function() {
  var route = this.subject();
  ok(route);
});

test('sets title correctly', function() {
  var route = this.subject();

  route.set('settings', {
    'forum_index_title': '',
    'forum_name': 'Forum Name',
  });

  route.send('didTransition');
  equal(document.title, 'Forum Name');

  route.set('settings', {
    'forum_index_title': 'Welcome to Forum!',
    'forum_name': 'Forum Name',
  });

  route.send('didTransition');
  equal(document.title, 'Welcome to Forum!');
});
