import Ember from 'ember';

export default Ember.Component.extend({
  isBusy: false,

  apiUrl: function() {
    return 'users/' + this.auth.get('user.id') + '/avatar';
  }.property(),

  avatarRPC: function(avatarType) {
    if (this.get('isBusy')) { return; }

    this.set('isBusy', true);

    var self = this;
    this.ajax.post(this.get('apiUrl'), {
      avatar: avatarType
    }).then(function(response) {
      if (self.isDestroyed) { return; }
      self.auth.set('user.avatar_hash', response.avatar_hash);
      self.toast.success(response.detail);
      self.get('options').setProperties(response.options);
    }, function(jqXHR) {
      if (self.isDestroyed) { return; }
      if (jqXHR.status === 400) {
        self.toast.error(jqXHR.responseJSON.detail);
      } else {
        self.toast.apiError(jqXHR);
      }
    }).finally(function() {
      if (self.isDestroyed) { return; }
      self.set('isBusy', false);
    });
  },

  actions: {
    setGravatar: function() {
      this.avatarRPC('gravatar');
    },

    setGenerated: function() {
      this.avatarRPC('generated');
    },

    goTo: function(component) {
      this.set('activeForm', component);
    }
  }
});
