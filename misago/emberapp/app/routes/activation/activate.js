import MisagoRoute from 'misago/routes/misago';

export default MisagoRoute.extend({
  model: function(params) {
    return this.ajax.post('auth/activate-account/' + params.user_id + '/' + params.token);
  },

  afterModel: function(model) {
    this.modal.show('login');
    this.toast.success(model.detail);
    return this.transitionTo('index');
  },

  actions: {
    loading: function() {
      this.set('title', gettext('Activating account...'));
      return true;
    },

    error: function(reason) {
      if (reason.status === 400) {
        this.toast.error(reason.responseJSON.detail);
        return this.transitionTo('activation');
      }

      return true;
    }
  }
});
