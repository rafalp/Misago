import Ember from 'ember';

export default Ember.Component.extend({
  tagName: 'form',

  isLoading: false,
  email: '',

  router: function() {
    return this.container.lookup('router:main');
  }.property(),

  submit: function() {
    if (this.get('isLoading')) {
      return false;
    }

    var email = Ember.$.trim(this.get('email'));

    if (email === "") {
      this.toast.warning(gettext("Enter e-mail address."));
      return false;
    }

    this.set('isLoading', true);

    var self = this;
    this.rpc.ajax(this.get('url'), {
      email: email
    }).then(function(requestingUser) {
      if (self.isDestroyed) { return; }
      self.success(requestingUser);
    }, function(jqXHR) {
      if (self.isDestroyed) { return; }
      self.error(jqXHR);
    }).finally(function() {
      if (self.isDestroyed) { return; }
      self.set('isLoading', false);
    });

    return false;
  },

  success: function(requestingUser) {
    this.sendAction('action', requestingUser);
    this.set('email', '');
  },

  error: function(jqXHR) {
    if (jqXHR.status === 400){
      var rejection = jqXHR.responseJSON;
      if (rejection.code === 'banned') {
        this.get('router').intermediateTransitionTo('error-banned', rejection.detail);
        this.set('email', '');
      } else {
        this.toast.error(rejection.detail);
      }
    } else {
      this.toast.apiError(jqXHR);
    }
  }
});
