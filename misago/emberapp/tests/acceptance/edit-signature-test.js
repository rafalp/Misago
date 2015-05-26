import Ember from 'ember';
import { module, test } from 'qunit';
import startApp from '../helpers/start-app';
import getToastMessage from '../helpers/toast-message';
import createUser from '../helpers/create-user';

var application, container, auth;

module('Acceptance: Edit Signature', {
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

test('/options/edit-signature form can be accessed', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  Ember.$.mockjax({
    url: '/api/users/' + user.id + '/signature/',
    status: 200,
    responseText: {
      'limit': 200,
      'signature': null
    }
  });

  assert.expect(2);

  visit('/options/edit-signature/');

  andThen(function() {
    assert.equal(currentPath(), 'options.signature');
    assert.ok(find('#editor-input'));
  });
});

test('/options/edit-signature form access is denied', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  Ember.$.mockjax({
    url: '/api/users/' + user.id + '/signature/',
    status: 403,
    responseText: {
      'detail': 'Nope!',
      'reason': '<p>For testing!</p>'
    }
  });

  assert.expect(3);

  visit('/options/edit-signature/');

  andThen(function() {
    assert.equal(currentPath(), 'options.signature');

    var errorLead = Ember.$.trim(find('.panel-error p.lead').text());
    assert.equal(errorLead, 'Nope!');

    var errorReason = Ember.$.trim(find('.panel-error p').last().text());
    assert.equal(errorReason, 'For testing!');
  });
});

test('/options/edit-signature form renders set signature', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  Ember.$.mockjax({
    url: '/api/users/' + user.id + '/signature/',
    status: 200,
    responseText: {
      'limit': 200,
      'signature': {
        'plain': 'Test signature.',
        'html': '<p>Test signature.</p>'
      }
    }
  });

  assert.expect(2);

  visit('/options/edit-signature/');

  andThen(function() {
    assert.equal(currentPath(), 'options.signature');

    var preview = Ember.$.trim(find('.misago-markup p').text());
    assert.equal(preview, 'Test signature.');
  });
});

test('/options/edit-signature form submit changes signature', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  Ember.$.mockjax({
    url: '/api/users/' + user.id + '/signature/',
    status: 200,
    type: 'GET',
    responseText: {
      'limit': 200,
      'signature': null
    }
  });

  Ember.$.mockjax({
    url: '/api/users/' + user.id + '/signature/',
    status: 200,
    type: 'POST',
    responseText: {
      'limit': 200,
      'signature': {
        'plain': 'Test signature.',
        'html': '<p>Test signature.</p>'
      }
    }
  });

  assert.expect(3);

  visit('/options/edit-signature/');
  click('.edit-signature-form .btn-primary');

  andThen(function() {
    assert.equal(currentPath(), 'options.signature');
    assert.equal(getToastMessage(), 'Your signature was updated.');

    var preview = Ember.$.trim(find('.misago-markup p').text());
    assert.equal(preview, 'Test signature.');
  });
});

test('/options/edit-signature form submit clears signature', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  Ember.$.mockjax({
    url: '/api/users/' + user.id + '/signature/',
    status: 200,
    type: 'GET',
    responseText: {
      'limit': 200,
      'signature': {
        'plain': 'Test signature.',
        'html': '<p>Test signature.</p>'
      }
    }
  });

  Ember.$.mockjax({
    url: '/api/users/' + user.id + '/signature/',
    status: 200,
    type: 'POST',
    responseText: {
      'limit': 200,
      'signature': null
    }
  });

  assert.expect(3);

  visit('/options/edit-signature/');
  click('.edit-signature-form .btn-primary');

  andThen(function() {
    assert.equal(currentPath(), 'options.signature');
    assert.equal(getToastMessage(), 'Your signature was cleared.');
    assert.ok(Ember.$('.misago-markup').length === 0);
  });
});

test('/options/edit-signature form submit errors', function(assert) {
  var user = createUser();
  auth.setProperties({
    'isAuthenticated': true,
    'user': user
  });

  Ember.$.mockjax({
    url: '/api/users/' + user.id + '/signature/',
    status: 200,
    type: 'GET',
    responseText: {
      'limit': 200,
      'signature': null
    }
  });

  Ember.$.mockjax({
    url: '/api/users/' + user.id + '/signature/',
    status: 400,
    type: 'POST',
    responseText: {
      'detail': 'Siggy is too long!'
    }
  });

  assert.expect(1);

  visit('/options/edit-signature/');
  click('.edit-signature-form .btn-primary');

  andThen(function() {
    assert.equal(getToastMessage(), 'Siggy is too long!');
  });
});
