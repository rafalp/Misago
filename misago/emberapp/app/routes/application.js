import MisagoRoute from 'misago/routes/misago';

export default MisagoRoute.extend({
  actions: {
    // Loading handler

    loading: function() {
      document.title = this.get('settings.forum_name');
      return true;
    },

    // Error handlers

    error: function(reason) {
      if (reason.status === 0) {
        this.set('title', gettext('Connection lost'));
        return this.intermediateTransitionTo('error-0');
      }

      if (typeof reason.responseJSON !== 'undefined' && typeof reason.responseJSON.ban !== 'undefined') {
        this.set('title', gettext('You are banned'));
        return this.intermediateTransitionTo('error-banned', reason.responseJSON.ban);
      }

      if (reason.status === 403) {
        this.set('title', gettext('Page not available'));

        var final_error = {status: 403, message: null};
        if (typeof reason.responseJSON !== 'undefined' && typeof reason.responseJSON.detail !== 'undefined' && reason.responseJSON.detail !== 'Permission denied') {
          final_error.message = reason.responseJSON.detail;
        }

        return this.intermediateTransitionTo('error-403', final_error);
      }

      if (reason.status === 404) {
        this.set('title', gettext('Page not found'));
        return this.intermediateTransitionTo('error-404');
      }

      this.set('title', gettext('Error'));
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

      this.toast.error(errorMessage);
    },

    showBan: function(ban) {
      this.set('title', gettext('You are banned'));
      this.intermediateTransitionTo('error-banned', ban);
    }
  }
});
