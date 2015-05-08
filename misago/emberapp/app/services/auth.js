import Ember from 'ember';

export default Ember.Service.extend({
  // State synchronization across tabs

  needsSync: false, // becomes true if auth state between tabs differs
  syncToUser: null, // becomes user obj to which we want to sync or null for anon

  syncSession: function() {
    this.session.setItem('auth-user', this.get('user'));
    this.session.setItem('auth-is-authenticated', this.get('isAuthenticated'));

    var self = this;
    this.session.watchItem('auth-is-authenticated', function(isAuthenticated) {
      self._handleAuthChange(isAuthenticated);
    });

    this.session.watchItem('auth-user', function(newUser) {
      self._handleUserChange(newUser);
    });
  }.on('init'),

  _handleAuthChange: function(isAuthenticated) {
    if (!this.get('needsSync')) {
      // display annoying "you were desynced" message
      this.set('needsSync', true);

      if (isAuthenticated) {
        this.set('syncToUser', Ember.Object.create(this.session.getItem('auth-user')));
      }
    }
  },

  _handleUserChange: function(newUser) {
    if (!this.get('needsSync')) {
      var userObj = Ember.Object.create(newUser);
      if (userObj.get('id') !== this.get('user.id')) {
        this.setProperties({
          'needsSync': true,
          'syncToUser': userObj,
        });
      } else {
        this.get('user').setProperties(newUser);
      }
    }
  },

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
