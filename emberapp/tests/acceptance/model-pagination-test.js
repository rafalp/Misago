import Ember from 'ember';
import { module, test } from 'qunit';
import startApp from '../helpers/start-app';
import createUser from '../helpers/create-user';
import { updateObjProps, paginatedJSON, rankJSON, userJSON } from '../helpers/api-mocks';

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

  var rank = rankJSON(3, {
    'name': 'Test Rank',
    'slug': 'test-rank',
    'is_tab': true
  });

  Ember.$.mockjax({
    url: '/api/ranks/',
    status: 200,
    responseText: [rank]
  });

  var users = [];
  for (var i = 1; i <= 20; i++) {
    users.push(userJSON(i, { 'rank': rank }));
  }

  var resultsJSON = paginatedJSON(users, 20, 2, 10, 5);
  resultsJSON.users = 10;

  Ember.$.mockjax({
    url: '/api/users/',
    data: {
      'list': 'rank',
      'rank': 'test-rank'
    },
    status: 200,
    responseText: resultsJSON
  });

  assert.expect(1);

  visit('/users/test-rank/1/');

  andThen(function() {
    assert.equal(currentPath(), 'users.rank.index');
  });
});

test('pagination displays next page', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  var rank = rankJSON(3, {
    'name': 'Test Rank',
    'slug': 'test-rank',
    'is_tab': true
  });

  Ember.$.mockjax({
    url: '/api/ranks/',
    status: 200,
    responseText: [rank]
  });

  var users = [];
  for (var i = 1; i <= 20; i++) {
    users.push(userJSON(i, { 'rank': rank }));
  }

  var resultsJSON = paginatedJSON(users, 20, 2, 10, 5);
  resultsJSON.users = 10;

  Ember.$.mockjax({
    url: '/api/users/',
    data: {
      'list': 'rank',
      'rank': 'test-rank',
      'page': 2,
    },
    status: 200,
    responseText: resultsJSON
  });

  assert.expect(1);

  visit('/users/test-rank/2/');

  andThen(function() {
    assert.equal(currentPath(), 'users.rank.page');
  });
});

test('pagination go to next page', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  var rank = rankJSON(3, {
    'name': 'Test Rank',
    'slug': 'test-rank',
    'is_tab': true
  });

  Ember.$.mockjax({
    url: '/api/ranks/',
    status: 200,
    responseText: [rank]
  });

  var users = [];
  for (var i = 1; i <= 20; i++) {
    users.push(userJSON(i, { 'rank': rank }));
  }

  var resultsJSON = paginatedJSON(users, 20, 2, 6, 2);
  resultsJSON.users = 10;

  Ember.$.mockjax({
    url: '/api/users/',
    data: {
      'list': 'rank',
      'rank': 'test-rank',
      'page': 2
    },
    status: 200,
    responseText: resultsJSON
  });

  resultsJSON = paginatedJSON(users, 20, 1, 6, 2);
  resultsJSON.users = 10;

  Ember.$.mockjax({
    url: '/api/users/',
    data: {
      'list': 'rank',
      'rank': 'test-rank'
    },
    status: 200,
    responseText: resultsJSON
  });

  assert.expect(2);

  visit('/users/test-rank/');
  click('.pager-aligned .btn-next-page:last');

  andThen(function() {
    assert.equal(currentURL(), '/users/test-rank/2');
    assert.equal(currentPath(), 'users.rank.page');
  });
});

test('pagination go to last page', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  var rank = rankJSON(3, {
    'name': 'Test Rank',
    'slug': 'test-rank',
    'is_tab': true
  });

  Ember.$.mockjax({
    url: '/api/ranks/',
    status: 200,
    responseText: [rank]
  });

  var users = [];
  for (var i = 1; i <= 20; i++) {
    users.push(userJSON(i, { 'rank': rank }));
  }

  var resultsJSON = paginatedJSON(users, 20, 3, 6, 2);
  resultsJSON.users = 10;

  Ember.$.mockjax({
    url: '/api/users/',
    data: {
      'list': 'rank',
      'rank': 'test-rank',
      'page': 3
    },
    status: 200,
    responseText: resultsJSON
  });

  resultsJSON = paginatedJSON(users, 20, 1, 6, 2);
  resultsJSON.users = 10;

  Ember.$.mockjax({
    url: '/api/users/',
    data: {
      'list': 'rank',
      'rank': 'test-rank'
    },
    status: 200,
    responseText: resultsJSON
  });

  assert.expect(2);

  visit('/users/test-rank/');
  click('.pager-aligned .btn-last-page');

  andThen(function() {
    assert.equal(currentURL(), '/users/test-rank/3');
    assert.equal(currentPath(), 'users.rank.page');
  });
});

test('pagination go to previous page', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  var rank = rankJSON(3, {
    'name': 'Test Rank',
    'slug': 'test-rank',
    'is_tab': true
  });

  Ember.$.mockjax({
    url: '/api/ranks/',
    status: 200,
    responseText: [rank]
  });

  var users = [];
  for (var i = 1; i <= 20; i++) {
    users.push(userJSON(i, { 'rank': rank }));
  }

  var resultsJSON = paginatedJSON(users, 20, 2, 6, 2);
  resultsJSON.users = 10;

  Ember.$.mockjax({
    url: '/api/users/',
    data: {
      'list': 'rank',
      'rank': 'test-rank',
      'page': 2
    },
    status: 200,
    responseText: resultsJSON
  });

  resultsJSON = paginatedJSON(users, 20, 3, 6, 2);
  resultsJSON.users = 10;

  Ember.$.mockjax({
    url: '/api/users/',
    data: {
      'list': 'rank',
      'rank': 'test-rank',
      'page': 3
    },
    status: 200,
    responseText: resultsJSON
  });

  assert.expect(2);

  visit('/users/test-rank/3/');
  click('.pager-aligned .btn-previous-page:last');

  andThen(function() {
    assert.equal(currentURL(), '/users/test-rank/2');
    assert.equal(currentPath(), 'users.rank.page');
  });
});

test('pagination go to first page', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  var rank = rankJSON(3, {
    'name': 'Test Rank',
    'slug': 'test-rank',
    'is_tab': true
  });

  Ember.$.mockjax({
    url: '/api/ranks/',
    status: 200,
    responseText: [rank]
  });

  var users = [];
  for (var i = 1; i <= 20; i++) {
    users.push(userJSON(i, { 'rank': rank }));
  }

  var resultsJSON = paginatedJSON(users, 20, 3, 6, 2);
  resultsJSON.users = 10;

  Ember.$.mockjax({
    url: '/api/users/',
    data: {
      'list': 'rank',
      'rank': 'test-rank',
      'page': 3
    },
    status: 200,
    responseText: resultsJSON
  });

  resultsJSON = paginatedJSON(users, 20, 1, 6, 2);
  resultsJSON.users = 10;

  Ember.$.mockjax({
    url: '/api/users/',
    data: {
      'list': 'rank',
      'rank': 'test-rank'
    },
    status: 200,
    responseText: resultsJSON
  });

  assert.expect(2);

  visit('/users/test-rank/3/');
  click('.pager-aligned .btn-first-page');

  andThen(function() {
    assert.equal(currentURL(), '/users/test-rank');
    assert.equal(currentPath(), 'users.rank.index');
  });
});
