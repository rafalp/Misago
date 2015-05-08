import Ember from 'ember';

export default Ember.Service.extend({
  // State synchronization across tabs

  needsSync: false, // becomes true if auth state between tabs differs
  syncToUser: false, // becomes user obj to which we want to sync or none for anon

  syncSession: function() {
    this.session.setItem('auth-user', this.get('user'));
    this.session.setItem('auth-is-authenticated', this.get('isAuthenticated'));

    var self = this;
    this.session.watchItem('auth-is-authenticated', function(isAuthenticated) {
      if (!self.get('needsSync')) {
        // display annoying "you were desynced" message
        self.set('needsSync', true);

        if (isAuthenticated) {
          self.set('syncToUser', Ember.Object.create(self.session.getItem('auth-user')));
        }
      }
    });
  }.on('init'),

  // Anon/auth state
  isAnonymous: Ember.computed.not('isAuthenticated'),

  logout: function() {
    this.session.setItem('auth-user', false);
    this.session.setItem('auth-is-authenticated', false);
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
