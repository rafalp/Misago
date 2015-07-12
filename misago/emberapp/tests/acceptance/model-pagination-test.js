import Ember from 'ember';
import { module, test } from 'qunit';
import startApp from '../helpers/start-app';
import createUser from '../helpers/create-user';

var application, container, auth;

module('Acceptance: Model Pagination Mixin', {
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

test('pagination redirects from explicit first page', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  Ember.$.mockjax({
    url: '/api/ranks/',
    status: 200,
    responseText: [{
      'id': 3,
      'name': 'Test Rank',
      'slug': 'test-rank',
      'description': '',
      'css_class': '',
      'is_tab': true
    }]
  });

  Ember.$.mockjax({
    url: '/api/users/?list=rank&rank=test-rank',
    status: 200,
    responseText: []
  });

  assert.expect(1);

  visit('/users/');

  andThen(function() {
    console.log(find('.nav-tabs').text())
    assert.equal(currentPath(), 'users.rank.index');
  });
});
