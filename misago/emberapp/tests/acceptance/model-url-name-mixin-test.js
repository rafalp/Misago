import Ember from 'ember';
import { module, test } from 'qunit';
import startApp from '../helpers/start-app';
import ModelUrlName from 'misago/mixins/model-url-name';

var application;

module('Acceptance: Page Title Mixin', {
  beforeEach: function() {
    application = startApp();
  },

  afterEach: function() {
    Ember.run(application, 'destroy');
    Ember.$.mockjax.clear();
  }
});

test('parseUrlName parses single word slug', function(assert) {
  assert.expect(2);

  var mixin = Ember.Object.extend(ModelUrlName).create();

  var parsed = mixin.parseUrlName('lorem-123');
  assert.equal(parsed.slug, 'lorem');
  assert.equal(parsed.id, '123');
});

test('parseUrlName parses two words slug', function(assert) {
  assert.expect(2);

  var mixin = Ember.Object.extend(ModelUrlName).create();

  var parsed = mixin.parseUrlName('lorem-ipsum-123');
  assert.equal(parsed.slug, 'lorem-ipsum');
  assert.equal(parsed.id, '123');
});

test('parseUrlName parses complex slugs', function(assert) {
  assert.expect(2);

  var mixin = Ember.Object.extend(ModelUrlName).create();

  var parsed = mixin.parseUrlName('lorem-123-ipsum-456-78');
  assert.equal(parsed.slug, 'lorem-123-ipsum-456');
  assert.equal(parsed.id, '78');
});

test('parseUrlName fails to parse invalid slugs', function(assert) {
  assert.expect(4);

  var mixin = Ember.Object.extend(ModelUrlName).create();

  assert.equal(mixin.parseUrlName('lorem.123'), false);
  assert.equal(mixin.parseUrlName('lorem-123-ipsum-456-abc'), false);
  assert.equal(mixin.parseUrlName('abc'), false);
  assert.equal(mixin.parseUrlName('123'), false);
});

test('getParsedUrlNameOr404 passes on valid slug', function(assert) {
  assert.expect(2);

  Ember.$.mockjax({
    url: '/api/users/42/',
    status: 403,
    responseText: {
      detail: 'Server was hit by Ember!'
    }
  });

  visit('user/misago-42/');

  andThen(function() {
    assert.equal(currentPath(), 'error-403');

    var errorMessage = Ember.$.trim(find('.error-message .lead').text());
    assert.equal(errorMessage, 'Server was hit by Ember!');
  });
});

test('getParsedUrlNameOr404 raises error 404 on invalid slug', function(assert) {
  assert.expect(1);

  visit('user/mis+ago-42/');

  andThen(function() {
    assert.equal(currentPath(), 'error-404');
  });
});

test('getParsedUrlNameOr404 redirects on outdated slug', function(assert) {
  assert.expect(2);

  Ember.$.mockjax({
    url: '/api/users/42/',
    status: 200,
    responseText: {
      id: '42',
      username: 'Miasgo',
      slug: 'miasgo'
    }
  });

  visit('user/misago-42/');

  andThen(function() {
    assert.equal(currentPath(), 'user');
    assert.ok(currentURL().indexOf('user/miasgo-42') !== -1);
  });
});
