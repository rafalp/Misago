import Ember from 'ember';
import { initialize } from '../../../initializers/dev-csrf-tokens';
import MisagoPreloadStore from '../../../utils/preloadstore';
import { module, test } from 'qunit';

var container, application;

var cookieName = MisagoPreloadStore.get('csrfCookieName');

var testCookieName = 'devcsrftokenCookie';
var testCookieValue = 't3stW0rk5';

var $element = null;

module('devCsrfTokensInitializer', {
  beforeEach: function() {
    // assert csrf token exists:
    MisagoPreloadStore.set('csrfCookieName', testCookieName);
    document.cookie = testCookieName + '=' + testCookieValue + ';';

    // set test element
    $element = Ember.$('<input type="hidden" name="csrfmiddlewaretoken">');
    Ember.$('#ember-testing').append($element);

    // prepare app
    Ember.run(function() {
      application = Ember.Application.create();
      container = application.__container__;
      application.deferReadiness();
    });
  },

  afterEach: function() {
    MisagoPreloadStore.set('csrfCookieName', cookieName);
    $element.remove();
  }
});

test('sets tokens on predefined forms', function(assert) {
  assert.expect(1);
  var done = assert.async();

  Ember.run(function() {
    initialize();
    assert.equal($element.val(), testCookieValue);
    done();
  });
});
