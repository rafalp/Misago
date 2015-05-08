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
        return this.intermediateTransitionTo('error-0');
      }

      if (typeof reason.responseJSON !== 'undefined' && typeof reason.responseJSON.ban !== 'undefined') {
        return this.intermediateTransitionTo('error-banned', reason.responseJSON.ban);
      }

      if (reason.status === 403) {
        var final_error = {status: 403, message: null};
        if (typeof reason.responseJSON !== 'undefined' && typeof reason.responseJSON.detail !== 'undefined' && reason.responseJSON.detail !== 'Permission denied') {
          final_error.message = reason.responseJSON.detail;
        }

        return this.intermediateTransitionTo('error-403', final_error);
      }

      if (reason.status === 404) {
        return this.intermediateTransitionTo('error-404');
      }

      this.set('title', gettext('Error'));
      return true;
    }
  }
});
