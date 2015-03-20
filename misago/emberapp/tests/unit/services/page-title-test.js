import {
  moduleFor,
  test
} from 'ember-qunit';

moduleFor('service:page-title', {
  needs: ['initializer:misago-settings']
});

test('it exists', function(assert) {
  var service = this.subject();
  assert.ok(service);
});

test('setTitle changes document title', function(assert) {
  assert.expect(5);

  var service = this.subject();
  service.set('forumName', 'Test Forum');

  // string argument
  service.setTitle('Welcome!');
  assert.equal(document.title, 'Welcome! | Test Forum');

  // object argument
  service.setTitle({title: 'Thread'});
  assert.equal(document.title, 'Thread | Test Forum');

  // object argument with parent
  service.setTitle({title: 'Test Thread', parent: 'Support'});
  assert.equal(document.title, 'Test Thread | Support | Test Forum');

  // object argument with page
  service.setTitle({title: 'Test Thread', page: 12});
  assert.equal(document.title, 'Test Thread (page 12) | Test Forum');

  // object argument with page and parent
  service.setTitle({title: 'Test Thread', page: 12, parent: 'Support'});
  assert.equal(document.title, 'Test Thread (page 12) | Support | Test Forum');
});

test('setPlaceholderTitle changes document title to one defined for index', function(assert) {
  assert.expect(1);

  var service = this.subject();
  service.set('forumName', 'Placeholder Test Forum');

  // no index title is set
  service.setPlaceholderTitle();
  assert.equal(document.title, 'Placeholder Test Forum');
});

test('setIndexTitle changes document title to one defined for index', function(assert) {
  assert.expect(2);

  var service = this.subject();
  service.set('forumName', 'Test Forum');

  // no index title is set
  service.setIndexTitle();
  assert.equal(document.title, 'Test Forum');

  // index title is set
  service.set('indexTitle', 'Test Forum Index');
  service.setIndexTitle();
  assert.equal(document.title, 'Test Forum Index');
});
