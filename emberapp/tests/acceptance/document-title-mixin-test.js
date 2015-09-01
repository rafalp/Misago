import Ember from 'ember';
import { module, test } from 'qunit';
import startApp from '../helpers/start-app';
import DocumentTitle from 'misago/mixins/document-title';

var application, container, store, title, forum_name;

module('Acceptance: Page Title Mixin', {
  beforeEach: function() {
    title = document.title;

    application = startApp();
    container = application.__container__;

    forum_name = container.lookup('misago:settings').forum_name;
  },

  afterEach: function() {
    document.title = title;
    container.lookup('misago:settings').forum_name = forum_name;

    Ember.run(application, 'destroy');
  }
});

test('setTitle changes document title', function(assert) {
  assert.expect(5);

  var TestRoute = Ember.Object.extend(DocumentTitle, {
    settings: container.lookup('misago:settings')
  });

  container.lookup('misago:settings').forum_name = 'Test Forum';

  var mixin = TestRoute.create();

  // string argument
  mixin.set('title', 'Welcome!');
  assert.equal(document.title, 'Welcome! | Test Forum');

  // object argument
  mixin.set('title', {title: 'Thread'});
  assert.equal(document.title, 'Thread | Test Forum');

  // object argument with parent
  mixin.set('title', {title: 'Test Thread', parent: 'Support'});
  assert.equal(document.title, 'Test Thread | Support | Test Forum');

  // object argument with page
  mixin.set('title', {title: 'Test Thread', page: 12});
  assert.equal(document.title, 'Test Thread (page 12) | Test Forum');

  // object argument with page and parent
  mixin.set('title', {title: 'Test Thread', page: 12, parent: 'Support'});
  assert.equal(document.title, 'Test Thread (page 12) | Support | Test Forum');
});
