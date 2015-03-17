import Ember from 'ember';
import ResetScroll from 'misago/mixins/reset-scroll';
import rpc from 'misago/utils/rpc';

export default Ember.Route.extend(ResetScroll, {
  model: function(params) {
    return rpc('activation/' + params.user_id + '/' + params.token + '/validate-token/');
  },

  afterModel: function(model) {
    this.send('openLoginModal');
    this.get('toast').success(model.detail);
    return this.transitionTo('index');
  },

  actions: {
    loading: function() {
      this.get('page-title').setTitle(gettext('Activating account...'));
      return true;
    },

    error: function(reason) {
      if (reason.status === 404) {
        this.get('toast').error(reason.responseJSON.detail);
        return this.transitionTo('activation');
      }

      return true;
    }
  }
});
