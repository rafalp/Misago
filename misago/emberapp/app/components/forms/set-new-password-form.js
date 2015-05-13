import Ember from 'ember';

export default Ember.Component.extend({
  tagName: 'form',

  isLoading: false,
  password: '',

  router: function() {
    return this.container.lookup('router:main');
  }.property(),

  url: function() {
    return 'auth/change-password/' + this.get('model.user_id') + '/' + this.get('model.token');
  }.property('model'),

  submit: function() {
    if (this.get('isLoading')) { return false; }

    var password = Ember.$.trim(this.get('password'));

    if (password === "") {
      this.toast.warning(gettext("Enter new password."));
      return false;
    }

    this.set('isLoading', true);

    var self = this;
    this.ajax.post(this.get('url'), {
      password: password
    }).then(function() {
      if (self.isDestroyed) { return; }
      self.success();
    }, function(jqXHR) {
      if (self.isDestroyed) { return; }
      self.error(jqXHR);
    }).finally(function() {
      self.set('isLoading', false);
    });

    return false;
  },

  success: function() {
    this.set('password', '');

    this.modal.show('login-modal');
    this.toast.success(gettext("Your password has been changed."));
  },

  error: function(jqXHR) {
    var rejection = jqXHR.responseJSON;
    if (jqXHR.status === 400){
      this.toast.error(rejection.detail);
    } else {
      if (jqXHR.status === 404) {
        this.toast.error(rejection.detail);
        this.get('router').transitionTo('forgotten-password');
      } else {
        this.toast.apiError(jqXHR);
      }
    }
  }
});
