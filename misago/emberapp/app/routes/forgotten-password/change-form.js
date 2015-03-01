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

    error: function(error) {
      if (error.status === 404) {
        this.send('flashError', error.detail);
        return this.transitionTo('forgotten-password');
      }

      return true;
    }
  }
});
