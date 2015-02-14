import Ember from 'ember';
import MisagoPreloadStore from 'misago/utils/preloadstore';

export default function getCsrfToken() {
  var regex = new RegExp(MisagoPreloadStore.get('csrfCookieName') + '\=([^;]*)');
  return Ember.get(document.cookie.match(regex), "1");
}
