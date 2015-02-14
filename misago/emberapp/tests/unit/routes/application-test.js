import {
  moduleFor,
  test
} from 'ember-qunit';

var document_title = document.title;

moduleFor('route:application', 'ApplicationRoute', {
  afterEach: function() {
    document.title = document_title;
  }
});

test('it exists', function(assert) {
  var route = this.subject();
  assert.ok(route);
});

test('error', function(assert) {
  var route = this.subject();
  route.set('settings', {'forum_name': 'Test Forum'});

  // generic error
  route.send('error', {status: 123});
  assert.equal(document.title, 'Error | Test Forum');
});

test('setTitle', function(assert) {
  var route = this.subject();
  route.set('settings', {'forum_name': 'Test Forum'});

  // string argument
  route.send('setTitle', 'Welcome!');
  assert.equal(document.title, 'Welcome! | Test Forum');

  // object argument
  route.send('setTitle', {title: 'Thread'});
  assert.equal(document.title, 'Thread | Test Forum');

  // object argument with parent
  route.send('setTitle', {title: 'Test Thread', parent: 'Support'});
  assert.equal(document.title, 'Test Thread | Support | Test Forum');

  // object argument with page
  route.send('setTitle', {title: 'Test Thread', page: 12});
  assert.equal(document.title, 'Test Thread (page 12) | Test Forum');

  // object argument with page and parent
  route.send('setTitle', {title: 'Test Thread', page: 12, parent: 'Support'});
  assert.equal(document.title, 'Test Thread (page 12) | Support | Test Forum');
});
