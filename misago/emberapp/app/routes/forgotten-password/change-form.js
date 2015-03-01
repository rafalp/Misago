import Ember from 'ember';
import ResetScroll from 'misago/mixins/reset-scroll';
import rpc from 'misago/utils/rpc';

export default Ember.Route.extend(ResetScroll, {
  model: function(params) {
    return rpc('change-password/' + params.user_id + '/' + params.token + '/validate-token/');
  },

  actions: {
    didTransition: function() {
      this.send('setTitle', gettext('Change forgotten password'));
      return true;
    },

    error: function(reason) {
      if (reason.status === 404) {
        this.send('flashError', reason.responseJSON.detail);
        return this.transitionTo('forgotten-password');
      }

      return true;
    }
  }
});
