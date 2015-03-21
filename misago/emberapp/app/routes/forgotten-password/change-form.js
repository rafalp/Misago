import MisagoRoute from 'misago/routes/misago';
import ResetScroll from 'misago/mixins/reset-scroll';

export default MisagoRoute.extend(ResetScroll, {
  model: function(params) {
    return this.rpc.ajax('change-password/' + params.user_id + '/' + params.token + '/validate-token');
  },

  actions: {
    didTransition: function() {
      this.set('title', gettext('Change forgotten password'));
    },

    error: function(reason) {
      if (reason.status === 404) {
        this.toast.error(reason.responseJSON.detail);
        return this.transitionTo('forgotten-password');
      }

      return true;
    }
  }
});
