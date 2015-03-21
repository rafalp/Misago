import MisagoRoute from 'misago/routes/misago';
import ResetScroll from 'misago/mixins/reset-scroll';

export default MisagoRoute.extend(ResetScroll, {
  model: function(params) {
    return this.rpc.ajax('activation/' + params.user_id + '/' + params.token + '/validate-token');
  },

  afterModel: function(model) {
    this.send('openLoginModal');
    this.toast.success(model.detail);
    return this.transitionTo('index');
  },

  actions: {
    loading: function() {
      this.set('title', gettext('Activating account...'));
      return true;
    },

    error: function(reason) {
      if (reason.status === 404) {
        this.toast.error(reason.responseJSON.detail);
        return this.transitionTo('activation');
      }

      return true;
    }
  }
});
