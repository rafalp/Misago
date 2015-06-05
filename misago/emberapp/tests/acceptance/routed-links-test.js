import Ember from 'ember';
import PreloadStore from 'misago/services/preload-store';
import { module, test } from 'qunit';
import startApp from '../helpers/start-app';

var application;

module('Acceptance: Routed Links Component', {
  beforeEach: function() {
    PreloadStore.set('staticUrl', '/static/');
    application = startApp();
  },
  afterEach: function() {
    Ember.run(application, 'destroy');
    Ember.$.mockjax.clear();
    PreloadStore.set('staticUrl', '/');
  }
});

test('app link within component gets routed by ember', function(assert) {
  assert.expect(1);

  Ember.$.mockjax({
    url: '/api/legal-pages/privacy-policy/',
    status: 403,
    responseText: {
      'ban': {
        'expires_on': null,
        'message': {
          'plain': 'You are banned. See /terms-of-service/.',
          'html': '<p>You are banned. See <a class="posted-link" href="/terms-of-service/">/terms-of-service/</a>.</p>'
        }
      }
    }
  });

  Ember.$.mockjax({
    url: '/api/legal-pages/terms-of-service/',
    responseText: {
      'id': 'terms-of-service',
      'title': 'Terms of service',
      'link': '',
      'body': '<p>Terms of service are working!</p>'
    }
  });

  visit('/privacy-policy');
  click('.error-message .posted-link');

  andThen(function() {
    assert.equal(currentPath(), 'terms-of-service');
  });
});
