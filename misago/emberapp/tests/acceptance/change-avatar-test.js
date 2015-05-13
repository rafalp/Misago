import Ember from 'ember';
import { module, test } from 'qunit';
import startApp from '../helpers/start-app';
import destroyModal from '../helpers/destroy-modal';
import getToastMessage from '../helpers/toast-message';
import createUser from '../helpers/create-user';

var application, container, auth;

module('Acceptance: Avatar Change Modal', {
  beforeEach: function() {
    application = startApp();
    container = application.__container__;
    auth = container.lookup('service:auth');
  },

  afterEach: function() {
    destroyModal();
    Ember.run(application, 'destroy');
    Ember.$.mockjax.clear();
  }
});


test('Change avatar modal handles no permission', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  var done = assert.async();
  assert.expect(1);

  Ember.$.mockjax({
    url: '/api/users/' + user.id + '/avatar/',
    status: 403,
    responseText: {
      'detail': 'Your avatar is locked.',
      'reason': ''
    }
  });

  visit('/');
  click('.navbar-user-nav .user-menu .dropdown-toggle');
  click('.navbar-user-nav .user-menu .editable-avatar');

  andThen(function() {
    var message = Ember.$.trim(find('#appModal .modal-message .lead').text());
    assert.equal(message, 'Your avatar is locked.');
    done();
  });
});


test('Minimal select avatar type form works', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  var done = assert.async();
  assert.expect(5);

  Ember.$.mockjax({
    url: '/api/users/' + user.id + '/avatar/',
    status: 200,
    responseText: {
      'generated': true,
      'gravatar': false,
      'crop_org': false,
      'crop_tmp': false,
      'upload': false,
      'galleries': false
    }
  });

  visit('/');
  click('.navbar-user-nav .user-menu .dropdown-toggle');
  click('.navbar-user-nav .user-menu .editable-avatar');

  andThen(function() {
    assert.ok(!find('#appModal .btn-gravatar').length);
    assert.ok(find('#appModal .btn-generated').length);
    assert.ok(!find('#appModal .btn-crop').length);
    assert.ok(!find('#appModal .btn-upload').length);
    assert.ok(!find('#appModal .btn-gallery').length);
    done();
  });
});


test('Complete select avatar type form works', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  var done = assert.async();
  assert.expect(5);

  Ember.$.mockjax({
    url: '/api/users/' + user.id + '/avatar/',
    status: 200,
    responseText: {
      'generated': true,
      'gravatar': true,
      'crop_org': true,
      'crop_tmp': true,
      'upload': true,
      'galleries': true
    }
  });

  visit('/');
  click('.navbar-user-nav .user-menu .dropdown-toggle');
  click('.navbar-user-nav .user-menu .editable-avatar');

  andThen(function() {
    assert.ok(find('#appModal .btn-gravatar').length);
    assert.ok(find('#appModal .btn-generated').length);
    assert.ok(find('#appModal .btn-crop').length);
    assert.ok(find('#appModal .btn-upload').length);
    assert.ok(find('#appModal .btn-gallery').length);
    done();
  });
});


test('Failed change to gravatar', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  var done = assert.async();
  assert.expect(1);

  Ember.$.mockjax({
    url: '/api/users/' + user.id + '/avatar/',
    status: 200,
    type: 'GET',
    responseText: {
      'generated': true,
      'gravatar': true,
      'crop_org': true,
      'crop_tmp': true,
      'upload': true,
      'galleries': true
    }
  });

  Ember.$.mockjax({
    url: '/api/users/' + user.id + '/avatar/',
    status: 400,
    type: 'POST',
    responseText: {
      'detail': 'Avatar change failed.',
    }
  });

  visit('/');
  click('.navbar-user-nav .user-menu .dropdown-toggle');
  click('.navbar-user-nav .user-menu .editable-avatar');
  click('#appModal .btn-gravatar');

  andThen(function() {
    assert.equal(getToastMessage(), 'Avatar change failed.');
    done();
  });
});


test('Changed avatar to gravatar', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  var done = assert.async();
  assert.expect(2);

  Ember.$.mockjax({
    url: '/api/users/' + user.id + '/avatar/',
    status: 200,
    type: 'GET',
    responseText: {
      'generated': true,
      'gravatar': true,
      'crop_org': true,
      'crop_tmp': true,
      'upload': true,
      'galleries': true
    }
  });

  Ember.$.mockjax({
    url: '/api/users/' + user.id + '/avatar/',
    status: 200,
    type: 'POST',
    responseText: {
      'detail': 'Avatar changed to Gravatar.',
      'avatar_hash': 'eeeeeeee',
      'options': {
        'generated': true,
        'gravatar': true,
        'crop_org': true,
        'crop_tmp': true,
        'upload': true,
        'galleries': true
      }
    }
  });

  visit('/');
  click('.navbar-user-nav .user-menu .dropdown-toggle');
  click('.navbar-user-nav .user-menu .editable-avatar');
  click('#appModal .btn-gravatar');

  andThen(function() {
    assert.equal(getToastMessage(), 'Avatar changed to Gravatar.');
    assert.equal(auth.get('user.avatar_hash'), 'eeeeeeee');
    done();
  });
});


test('Failed change to generated', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  var done = assert.async();
  assert.expect(1);

  Ember.$.mockjax({
    url: '/api/users/' + user.id + '/avatar/',
    status: 200,
    type: 'GET',
    responseText: {
      'generated': true,
      'gravatar': true,
      'crop_org': true,
      'crop_tmp': true,
      'upload': true,
      'galleries': true
    }
  });

  Ember.$.mockjax({
    url: '/api/users/' + user.id + '/avatar/',
    status: 400,
    type: 'POST',
    responseText: {
      'detail': 'Avatar change failed.',
    }
  });

  visit('/');
  click('.navbar-user-nav .user-menu .dropdown-toggle');
  click('.navbar-user-nav .user-menu .editable-avatar');
  click('#appModal .btn-generated');

  andThen(function() {
    assert.equal(getToastMessage(), 'Avatar change failed.');
    done();
  });
});


test('Changed avatar to generated', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  var done = assert.async();
  assert.expect(2);

  Ember.$.mockjax({
    url: '/api/users/' + user.id + '/avatar/',
    status: 200,
    type: 'GET',
    responseText: {
      'generated': true,
      'gravatar': true,
      'crop_org': true,
      'crop_tmp': true,
      'upload': true,
      'galleries': true
    }
  });

  Ember.$.mockjax({
    url: '/api/users/' + user.id + '/avatar/',
    status: 200,
    type: 'POST',
    responseText: {
      'detail': 'Avatar changed to generated.',
      'avatar_hash': 'eeeeeeee',
      'options': {
        'generated': true,
        'gravatar': true,
        'crop_org': true,
        'crop_tmp': true,
        'upload': true,
        'galleries': true
      }
    }
  });

  visit('/');
  click('.navbar-user-nav .user-menu .dropdown-toggle');
  click('.navbar-user-nav .user-menu .editable-avatar');
  click('#appModal .btn-generated');

  andThen(function() {
    assert.equal(getToastMessage(), 'Avatar changed to generated.');
    assert.equal(auth.get('user.avatar_hash'), 'eeeeeeee');
    done();
  });
});


test('Failed to pick avatar from gallery', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  var done = assert.async();
  assert.expect(1);

  Ember.$.mockjax({
    url: '/api/users/' + user.id + '/avatar/',
    status: 200,
    type: 'GET',
    responseText: {
      'generated': true,
      'gravatar': true,
      'crop_org': true,
      'crop_tmp': true,
      'upload': true,
      'galleries': [
        {
          'name': 'TestGallery',
          'images': [
            'some-image.jpg'
          ]
        }
      ]
    }
  });

  Ember.$.mockjax({
    url: '/api/users/' + user.id + '/avatar/',
    status: 400,
    type: 'POST',
    responseText: {
      'detail': 'Failed to pick gallery avatar.',
    }
  });

  visit('/');
  click('.navbar-user-nav .user-menu .dropdown-toggle');
  click('.navbar-user-nav .user-menu .editable-avatar');
  click('#appModal .btn-gallery');
  click('#appModal .col-sm-3 .btn');

  andThen(function() {
    assert.equal(getToastMessage(), 'Failed to pick gallery avatar.');
    done();
  });
});


test('Picked avatar from gallery', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  var done = assert.async();
  assert.expect(2);

  Ember.$.mockjax({
    url: '/api/users/' + user.id + '/avatar/',
    status: 200,
    type: 'GET',
    responseText: {
      'generated': true,
      'gravatar': true,
      'crop_org': true,
      'crop_tmp': true,
      'upload': true,
      'galleries': [
        {
          'name': 'TestGallery',
          'images': [
            'some-image.jpg'
          ]
        }
      ]
    }
  });

  Ember.$.mockjax({
    url: '/api/users/' + user.id + '/avatar/',
    status: 200,
    type: 'POST',
    responseText: {
      'detail': 'Avatar changed to gallery.',
      'avatar_hash': 'eeeeeeee',
      'options': {
        'generated': true,
        'gravatar': true,
        'crop_org': true,
        'crop_tmp': true,
        'upload': true,
        'galleries': true
      }
    }
  });

  visit('/');
  click('.navbar-user-nav .user-menu .dropdown-toggle');
  click('.navbar-user-nav .user-menu .editable-avatar');
  click('#appModal .btn-gallery');
  click('#appModal .col-sm-3 .btn');

  andThen(function() {
    assert.equal(getToastMessage(), 'Avatar changed to gallery.');
    assert.equal(auth.get('user.avatar_hash'), 'eeeeeeee');
    done();
  });
});


test('Canceled pick from gallery', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  var done = assert.async();
  assert.expect(1);

  Ember.$.mockjax({
    url: '/api/users/' + user.id + '/avatar/',
    status: 200,
    type: 'GET',
    responseText: {
      'generated': true,
      'gravatar': true,
      'crop_org': true,
      'crop_tmp': true,
      'upload': true,
      'galleries': [
        {
          'name': 'TestGallery',
          'images': ['some-image.png']
        }
      ]
    }
  });

  visit('/');
  click('.navbar-user-nav .user-menu .dropdown-toggle');
  click('.navbar-user-nav .user-menu .editable-avatar');
  click('#appModal .btn-gallery');
  click('#appModal .btn-block');

  andThen(function() {
    assert.ok(find('#appModal .btn-gravatar').length);
    done();
  });
});
