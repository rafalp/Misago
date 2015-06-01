import Ember from 'ember';
import { module, test } from 'qunit';
import startApp from '../helpers/start-app';
import getToastMessage from '../helpers/toast-message';
import createUser from '../helpers/create-user';

var application, container, auth;

module('Acceptance: Change Username', {
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

test('/options/change-username form can be accessed', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  Ember.$.mockjax({
    url: '/api/users/' + user.id + '/username/',
    status: 200,
    responseText: {
      'length_min': 2,
      'length_max': 20,
      'changes_left': 2,
      'next_on': null
    }
  });

  Ember.$.mockjax({
    url: '/api/username-changes/',
    status: 200,
    responseText: {
      'count': 0,
      'next': null,
      'previous': null,
      'results': []
    }
  });

  assert.expect(3);

  visit('/options/change-username/');

  andThen(function() {
    assert.equal(currentPath(), 'options.username');
    assert.ok(find('#id_username'));

    var listMessage = Ember.$.trim(find('.last-username-changes .list-group-item').text());
    assert.equal(listMessage, 'Your username was never changed.');
  });
});

test('/options/change-username form handles backend error', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  Ember.$.mockjax({
    url: '/api/users/' + user.id + '/username/',
    status: 403,
    responseText: {
      'detail': 'Nope!'
    }
  });

  Ember.$.mockjax({
    url: '/api/username-changes/',
    status: 200,
    responseText: {
      'count': 0,
      'next': null,
      'previous': null,
      'results': []
    }
  });

  assert.expect(3);

  visit('/options/change-username/');

  andThen(function() {
    assert.equal(currentPath(), 'options.username');

    var errorMessage = Ember.$.trim(find('.error-message p').text());
    assert.equal(errorMessage, 'Nope!');

    var listMessage = Ember.$.trim(find('.last-username-changes .list-group-item').text());
    assert.equal(listMessage, 'Your username was never changed.');
  });
});

test('/options/change-username disallows username change', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  var nextOn = moment();
  nextOn.add(7, 'days');

  Ember.$.mockjax({
    url: '/api/users/' + user.id + '/username/',
    status: 200,
    responseText: {
      'length_min': 2,
      'length_max': 20,
      'changes_left': 0,
      'next_on': nextOn.format()
    }
  });

  Ember.$.mockjax({
    url: '/api/username-changes/',
    status: 200,
    responseText: {
      'count': 0,
      'next': null,
      'previous': null,
      'results': []
    }
  });

  assert.expect(4);

  visit('/options/change-username/');

  andThen(function() {
    assert.equal(currentPath(), 'options.username');

    var errorMessage = Ember.$.trim(find('.panel-body p').first().text());
    assert.equal(errorMessage, "You can't change your username now.");

    var expiresMessage = Ember.$.trim(find('.panel-body p').last().text());
    assert.equal(expiresMessage, 'Next change will be possible in 7 days.');

    var listMessage = Ember.$.trim(find('.last-username-changes .list-group-item').text());
    assert.equal(listMessage, 'Your username was never changed.');
  });
});

test('/options/change-username changes username', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  var nextOn = moment();
  nextOn.add(7, 'days');

  Ember.$.mockjax({
    url: '/api/users/' + user.id + '/username/',
    status: 200,
    type: 'GET',
    responseText: {
      'length_min': 2,
      'length_max': 20,
      'changes_left': 3,
      'next_on': null
    }
  });

  Ember.$.mockjax({
    url: '/api/users/' + user.id + '/username/',
    status: 200,
    type: 'POST',
    responseText: {
      'username': 'NewName',
      'slug': 'newname',
      'options': {
        'length_min': 2,
        'length_max': 20,
        'changes_left': 3,
        'next_on': null
      }
    }
  });

  Ember.$.mockjax({
    url: '/api/username-changes/',
    status: 200,
    responseText: {
      'count': 0,
      'next': null,
      'previous': null,
      'results': []
    }
  });

  assert.expect(4);

  visit('/options/change-username/');
  fillIn('#id_username', 'NewName');
  click('.panel-form .panel-footer .btn-primary');

  andThen(function() {
    assert.equal(currentPath(), 'options.username');
    assert.equal(getToastMessage(), 'Your username has been changed.');

    var listedUsername = Ember.$.trim(find('.last-username-changes .item-name').text());
    assert.equal(listedUsername, 'NewName');

    assert.ok(find('.last-username-changes').text().indexOf('BobBoberson') !== -1);
  });
});

test('/options/change-username handles API error', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  var nextOn = moment();
  nextOn.add(7, 'days');

  Ember.$.mockjax({
    url: '/api/users/' + user.id + '/username/',
    status: 200,
    type: 'GET',
    responseText: {
      'length_min': 2,
      'length_max': 20,
      'changes_left': 3,
      'next_on': null
    }
  });

  Ember.$.mockjax({
    url: '/api/users/' + user.id + '/username/',
    status: 400,
    type: 'POST',
    responseText: {
      'detail': 'Not good new name.'
    }
  });

  Ember.$.mockjax({
    url: '/api/username-changes/',
    status: 200,
    responseText: {
      'count': 0,
      'next': null,
      'previous': null,
      'results': []
    }
  });

  assert.expect(3);

  visit('/options/change-username/');
  fillIn('#id_username', 'NewName');
  click('.panel-form .panel-footer .btn-primary');

  andThen(function() {
    assert.equal(currentPath(), 'options.username');
    assert.equal(getToastMessage(), 'Not good new name.');
    assert.equal(find('.last-username-changes').text().indexOf('NewName'), -1);
  });
});

test('/options/change-username handles empty form submit', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  var nextOn = moment();
  nextOn.add(7, 'days');

  Ember.$.mockjax({
    url: '/api/users/' + user.id + '/username/',
    status: 200,
    type: 'GET',
    responseText: {
      'length_min': 2,
      'length_max': 20,
      'changes_left': 3,
      'next_on': null
    }
  });

  Ember.$.mockjax({
    url: '/api/username-changes/',
    status: 200,
    responseText: {
      'count': 0,
      'next': null,
      'previous': null,
      'results': []
    }
  });

  assert.expect(2);

  visit('/options/change-username/');
  click('.panel-form .panel-footer .btn-primary');

  andThen(function() {
    assert.equal(currentPath(), 'options.username');
    assert.equal(getToastMessage(), 'Enter new username.');
  });
});

test('/options/change-username handles too long username', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  var nextOn = moment();
  nextOn.add(7, 'days');

  Ember.$.mockjax({
    url: '/api/users/' + user.id + '/username/',
    status: 200,
    type: 'GET',
    responseText: {
      'length_min': 2,
      'length_max': 5,
      'changes_left': 3,
      'next_on': null
    }
  });

  Ember.$.mockjax({
    url: '/api/username-changes/',
    status: 200,
    responseText: {
      'count': 0,
      'next': null,
      'previous': null,
      'results': []
    }
  });

  assert.expect(3);

  visit('/options/change-username/');
  fillIn('#id_username', 'NewNameTooLong');
  click('.panel-form .panel-footer .btn-primary');

  andThen(function() {
    assert.equal(currentPath(), 'options.username');
    assert.equal(getToastMessage(), 'Form contains errors.');

    var validationMessage = Ember.$.trim(find('.panel-form .form-group .help-block.errors').text());
    assert.equal(validationMessage, 'Username cannot be longer than 5 characters.');
  });
});

test('/options/change-username handles too short username', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  var nextOn = moment();
  nextOn.add(7, 'days');

  Ember.$.mockjax({
    url: '/api/users/' + user.id + '/username/',
    status: 200,
    type: 'GET',
    responseText: {
      'length_min': 12,
      'length_max': 25,
      'changes_left': 3,
      'next_on': null
    }
  });

  Ember.$.mockjax({
    url: '/api/username-changes/',
    status: 200,
    responseText: {
      'count': 0,
      'next': null,
      'previous': null,
      'results': []
    }
  });

  assert.expect(3);

  visit('/options/change-username/');
  fillIn('#id_username', 'TooShort');
  click('.panel-form .panel-footer .btn-primary');

  andThen(function() {
    assert.equal(currentPath(), 'options.username');
    assert.equal(getToastMessage(), 'Form contains errors.');

    var validationMessage = Ember.$.trim(find('.panel-form .form-group .help-block.errors').text());
    assert.equal(validationMessage, 'Username must be at least 12 characters long.');
  });
});

test('/options/change-username handles invalid username', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  var nextOn = moment();
  nextOn.add(7, 'days');

  Ember.$.mockjax({
    url: '/api/users/' + user.id + '/username/',
    status: 200,
    type: 'GET',
    responseText: {
      'length_min': 2,
      'length_max': 25,
      'changes_left': 3,
      'next_on': null
    }
  });

  Ember.$.mockjax({
    url: '/api/username-changes/',
    status: 200,
    responseText: {
      'count': 0,
      'next': null,
      'previous': null,
      'results': []
    }
  });

  assert.expect(3);

  visit('/options/change-username/');
  fillIn('#id_username', 'us3rn#me');
  click('.panel-form .panel-footer .btn-primary');

  andThen(function() {
    assert.equal(currentPath(), 'options.username');
    assert.equal(getToastMessage(), 'Form contains errors.');

    var validationMessage = Ember.$.trim(find('.panel-form .form-group .help-block.errors').text());
    assert.equal(validationMessage, 'Username can only contain latin alphabet letters and digits.');
  });
});

test('/options/change-username handles same username', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  var nextOn = moment();
  nextOn.add(7, 'days');

  Ember.$.mockjax({
    url: '/api/users/' + user.id + '/username/',
    status: 200,
    type: 'GET',
    responseText: {
      'length_min': 2,
      'length_max': 25,
      'changes_left': 3,
      'next_on': null
    }
  });

  Ember.$.mockjax({
    url: '/api/username-changes/',
    status: 200,
    responseText: {
      'count': 0,
      'next': null,
      'previous': null,
      'results': []
    }
  });

  assert.expect(3);

  visit('/options/change-username/');
  fillIn('#id_username', user.get('username'));
  click('.panel-form .panel-footer .btn-primary');

  andThen(function() {
    assert.equal(currentPath(), 'options.username');
    assert.equal(getToastMessage(), 'Form contains errors.');

    var validationMessage = Ember.$.trim(find('.panel-form .form-group .help-block.errors').text());
    assert.equal(validationMessage, 'New username is same as current one.');
  });
});

test('/options/change-username displays filtered history', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  var nextOn = moment();
  nextOn.add(7, 'days');

  Ember.$.mockjax({
    url: '/api/users/' + user.id + '/username/',
    status: 200,
    type: 'GET',
    responseText: {
      'length_min': 2,
      'length_max': 25,
      'changes_left': 3,
      'next_on': null
    }
  });

  Ember.$.mockjax({
    url: '/api/username-changes/',
    status: 200,
    responseText: {
      'count': 0,
      'next': null,
      'previous': null,
      'results': [
        {
            "id": 26,
            "user": {
                "id": 42,
                "username": "LoremIpsum",
                "slug": "loremipsum",
                "avatar_hash": "b03dc23d"
            },
            "changed_by": {
                "id": 42,
                "username": "LoremIpsum",
                "slug": "loremipsum",
                "avatar_hash": "b03dc23d"
            },
            "changed_by_username": "LoremIpsum",
            "changed_by_slug": "loremipsum",
            "changed_on": moment().format(),
            "new_username": "GoodName",
            "old_username": "BobBoberson"
        },
        {
            "id": 27,
            "user": {
                "id": 40,
                "username": "LoremIpsum",
                "slug": "loremipsum",
                "avatar_hash": "b03dc23d"
            },
            "changed_by": {
                "id": 42,
                "username": "LoremIpsum",
                "slug": "loremipsum",
                "avatar_hash": "b03dc23d"
            },
            "changed_by_username": "LoremIpsum",
            "changed_by_slug": "loremipsum",
            "changed_on": moment().format(),
            "new_username": "WrongName",
            "old_username": "BobBoberson"
        }
      ]
    }
  });

  assert.expect(4);

  visit('/options/change-username/');

  andThen(function() {
    assert.equal(currentPath(), 'options.username');
    assert.equal(find('.last-username-changes .list-group-item').length, 1);

    assert.ok(find('.last-username-changes').text().indexOf('GoodName') !== -1);
    assert.equal(find('.last-username-changes').text().indexOf('WrongName'), -1);
  });
});
