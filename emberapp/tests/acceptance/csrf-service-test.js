import Ember from 'ember';
import { module, test } from 'qunit';
import startApp from '../helpers/start-app';

var application, store, cookie, service;

module('Acceptance: CSRF Service', {
  beforeEach: function() {
    application = startApp();
    var container = application.__container__;

    store = container.lookup('service:preload-store');
    cookie = store.get('csrfCookieName');

    service = container.lookup('service:csrf');
  },

  afterEach: function() {
    Ember.run(application, 'destroy');
    store.set('csrfCookieName', cookie);
  }
});

test('cookieName property is valid csrf cookie name', function(assert) {
  assert.expect(2);

  store.set('csrfCookieName', 'testCSRFCookie');
  assert.equal(service.get('cookieName'), 'testCSRFCookie');

  store.set('csrfCookieName', 'wololoLolo');
  assert.equal(service.get('cookieName'), 'wololoLolo');
});

test('token property is valid csrf token', function(assert) {
  assert.expect(1);

  var cookieName = 'validcsrfcookie';
  var token = 'v4l1dc5rft0k3n';

  document.cookie = cookieName + '=' + token + ';';

  store.set('csrfCookieName', cookieName);
  assert.equal(service.get('token'), token);
});

test('updateFormToken updates csrf token in given form', function(assert) {
  assert.expect(1);

  var $form = Ember.$('<form>');
  $form.append(Ember.$('<input type="hidden" name="csrfmiddlewaretoken" value="oldtoken">'));

  var cookieName = 'insertedcsrfcookie';
  var token = 'insertedtoken';

  document.cookie = cookieName + '=' + token + ';';
  store.set('csrfCookieName', cookieName);

  service.updateFormToken($form);

  assert.equal($form.find('input').val(), token);
});
