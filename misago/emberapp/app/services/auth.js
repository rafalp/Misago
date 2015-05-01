import Ember from 'ember';

export default Ember.Service.extend({
  isAnonymous: Ember.computed.not('isAuthenticated'),

  logout: function() {
    Ember.$('#hidden-logout-form').submit();
  },

  // Utils for triggering 403 error

  _throw: function(message) {
    throw {
      status: 403,
      responseJSON: {
        detail: message
      }
    };
  },

  denyAuthenticated: function(message) {
    if (this.get('isAuthenticated')) {
      this._throw(message || gettext('This page is not available to signed in users.'));
    }
  },

  denyAnonymous: function(message) {
    if (this.get('isAnonymous')) {
      this._throw(message || gettext('This page is not available to guests.'));
    }
  }
});
