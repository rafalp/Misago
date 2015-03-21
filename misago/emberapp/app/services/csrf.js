import Ember from 'ember';
import ENV from '../config/environment';

export default Ember.Object.extend({
  cookieName: function() {
    return this.preloadStore.get('csrfCookieName');
  }.property.volatile(),

  token: function() {
    var regex = new RegExp(this.get('cookieName') + '\=([^;]*)');
    return Ember.get(document.cookie.match(regex), "1");
  }.property().volatile(),

  init: function() {
    if (ENV.environment !== 'production') {
      // set initial CSRF tokens on preloaded forms in dev
      Ember.$('input[name=csrfmiddlewaretoken]').val(this.get('token'));
    }
  },

  updateFormToken: function($form) {
    $form.find('input[name=csrfmiddlewaretoken]').val(this.get('token'));
  }
});
