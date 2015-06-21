import MisagoRoute from 'misago/routes/misago';

export default MisagoRoute.extend({
  model: function(params) {
    return this.ajax.post('users/' + this.get('auth.user.id') + '/change-password', {
      'token': params.token
    });
  },

  afterModel: function(model) {
    this.toast.success(model.detail);
    return this.transitionTo('options.password');
  },

  actions: {
    error: function(reason) {
      if (reason.status === 400) {
        this.toast.error(reason.responseJSON.detail);
        return this.transitionTo('options.password');
      }

      return true;
    }
  }
});
