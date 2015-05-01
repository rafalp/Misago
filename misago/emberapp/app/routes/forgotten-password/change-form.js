import MisagoRoute from 'misago/routes/misago';

export default MisagoRoute.extend({
  model: function(params) {
    return this.ajax.get('auth/change-password/' + params.user_id + '/' + params.token);
  },

  actions: {
    didTransition: function() {
      this.set('title', gettext('Change forgotten password'));
    },

    error: function(reason) {
      if (reason.status === 400) {
        this.toast.error(reason.responseJSON.detail);
        return this.transitionTo('forgotten-password');
      }

      return true;
    }
  }
});
