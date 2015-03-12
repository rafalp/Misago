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
      return false;
    },

    // Error handler

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

    showBan: function(ban) {
      this.send('setTitle', gettext('You are banned'));
      this.intermediateTransitionTo('error-banned', ban);
      return false;
    },

    // Auth

    openLoginModal: function() {
      this.controllerFor("loginModal").send('open');
      return false;
    },

    logOut: function() {
      this.get('auth').logout();
      Ember.$('#hidden-logout-form').submit();
      return false;
    }
  }
});
