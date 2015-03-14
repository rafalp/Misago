import getCsrfToken from '../../../utils/csrf';
import MisagoPreloadStore from '../../../utils/preloadstore';
import { module, test } from 'qunit';

var cookieName = MisagoPreloadStore.get('csrfCookieName');

module('csrf', {
  afterEach: function() {
    MisagoPreloadStore.set('csrfCookieName', cookieName);
  }
});

test('getCsrfToken function returns csrf token', function(assert) {
  assert.expect(1);

  var cookieName = 'validcsrfcookie';
  var token = 'v4l1dc5rft0k3n';

  MisagoPreloadStore.set('csrfCookieName', cookieName);

  document.cookie = cookieName + '=' + token + ';';
  assert.equal(getCsrfToken(), token);
});

test('getCsrfToken function returns undefined for non-existing cookie', function(assert) {
  assert.expect(1);

  MisagoPreloadStore.set('csrfCookieName', 'n0n3x15t1ng');
  assert.equal(getCsrfToken(), undefined);
});
