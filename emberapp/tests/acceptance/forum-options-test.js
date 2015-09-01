import Ember from 'ember';
import { module, test } from 'qunit';
import startApp from '../helpers/start-app';
import getToastMessage from '../helpers/toast-message';
import createUser from '../helpers/create-user';

var application, container, auth;

module('Acceptance: Forum Options', {
  beforeEach: function() {
    application = startApp();
    container = application.__container__;
    auth = container.lookup('service:auth');
  },
  afterEach: function() {
    Ember.run(application, 'destroy');
    Ember.$.mockjax.clear();
  }
});

test('visiting /options redirects to /options/forum-options', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  assert.expect(1);

  visit('/options');

  andThen(function() {
    assert.equal(currentPath(), 'options.forum');
  });
});

test('/options/forum-options form can be submitted', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  Ember.$.mockjax({
    url: '/api/users/' + user.id + '/forum-options/',
    status: 200,
    responseText: {
      'detail': 'API endpoint was called!'
    }
  });

  assert.expect(1);

  visit('/options/forum-options/');
  click('.panel-form .panel-body .btn');
  click('.panel-form .panel-footer .btn-primary');

  andThen(function() {
    assert.equal(getToastMessage(), 'API endpoint was called!');
  });
});
