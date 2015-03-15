import Ember from 'ember';

export default Ember.Route.extend({
  actions: {
    setTitle: function(title) {
      if (typeof title === 'string') {
        title = {title: title};
      }

      var complete_title = title.title;

      if (typeof title.page !== 'undefined') {
        complete_title += ' (' + interpolate(gettext('page %(page)s'), {page:title.page}, true) + ')';
      }

      if (typeof title.parent !== 'undefined') {
        complete_title += ' | ' + title.parent;
      }

      complete_title += ' | ' + this.get('settings.forum_name');

      document.title = complete_title;
    },

    // Error handlers

    error: function(reason) {
      if (reason.status === 0) {
        this.send('setTitle', gettext('Connection lost'));
        return this.intermediateTransitionTo('error-0');
      }

      if (typeof reason.responseJSON !== 'undefined' && typeof reason.responseJSON.ban !== 'undefined') {
        this.send('setTitle', gettext('You are banned'));
        return this.intermediateTransitionTo('error-banned', reason.responseJSON.ban);
      }

      if (reason.status === 403) {
        this.send('setTitle', gettext('Page not available'));

        var final_error = {status: 403, message: null};
        if (typeof reason.responseJSON !== 'undefined' && typeof reason.responseJSON.detail !== 'undefined' && reason.responseJSON.detail !== 'Permission denied') {
          final_error.message = reason.responseJSON.detail;
        }

        return this.intermediateTransitionTo('error-403', final_error);
      }

      if (reason.status === 404) {
        this.send('setTitle', gettext('Page not found'));
        return this.intermediateTransitionTo('error-404');
      }

      this.send('setTitle', gettext('Error'));
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
      this.send('setTitle', gettext('You are banned'));
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
