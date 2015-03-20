import Ember from 'ember';

export default Ember.Route.extend({
  actions: {
    // Loading handler

    loading: function() {
      this.get('page-title').setPlaceholderTitle();
      return true;
    },

    // Error handlers

    error: function(reason) {
      if (reason.status === 0) {
        this.get('page-title').setTitle(gettext('Connection lost'));
        return this.intermediateTransitionTo('error-0');
      }

      if (typeof reason.responseJSON !== 'undefined' && typeof reason.responseJSON.ban !== 'undefined') {
        this.get('page-title').setTitle(gettext('You are banned'));
        return this.intermediateTransitionTo('error-banned', reason.responseJSON.ban);
      }

      if (reason.status === 403) {
        this.get('page-title').setTitle(gettext('Page not available'));

        var final_error = {status: 403, message: null};
        if (typeof reason.responseJSON !== 'undefined' && typeof reason.responseJSON.detail !== 'undefined' && reason.responseJSON.detail !== 'Permission denied') {
          final_error.message = reason.responseJSON.detail;
        }

        return this.intermediateTransitionTo('error-403', final_error);
      }

      if (reason.status === 404) {
        this.get('page-title').setTitle(gettext('Page not found'));
        return this.intermediateTransitionTo('error-404');
      }

      this.get('page-title').setTitle(gettext('Error'));
      return true;
    },

    toastError: function(reason) {
      var errorMessage = gettext('Unknown error has occured.');

      if (reason.status === 0) {
        errorMessage = gettext('Lost connection with application.');
      }

      if (reason.status === 403) {
        if (typeof reason.responseJSON !== 'undefined' && typeof reason.responseJSON.detail !== 'undefined' && reason.responseJSON.detail !== 'Permission denied') {
          errorMessage = reason.responseJSON.detail;
        } else {
          errorMessage = gettext("You don't have permission to perform this action.");
        }
      }

      if (reason.status === 404) {
        errorMessage = gettext('Action link is invalid.');
      }

      this.get('toast').error(errorMessage);
    },

    showBan: function(ban) {
      this.get('page-title').setTitle(gettext('You are banned'));
      this.intermediateTransitionTo('error-banned', ban);
    },

    // Auth

    openLoginModal: function() {
      this.controllerFor("loginModal").send('open');
    },

    logOut: function() {
      this.get('auth').logout();
      Ember.$('#hidden-logout-form').submit();
    }
  }
});
