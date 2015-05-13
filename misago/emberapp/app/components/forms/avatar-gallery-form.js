import Ember from 'ember';

export default Ember.Component.extend({
  classNames: 'avatar-galleries',

  isBusy: false,
  activeItem: null,

  apiUrl: function() {
    return 'users/' + this.auth.get('user.id') + '/avatar';
  }.property(),

  actions: {
    setAvatar: function(image) {
      if (this.get('isBusy')) { return; }

      this.set('isBusy', true);
      this.set('activeItem', image);

      var self = this;
      this.ajax.post(this.get('apiUrl'), {
        avatar: 'galleries',
        image: image
      }).then(function(response) {
        if (self.isDestroyed) { return; }
        self.auth.set('user.avatar_hash', response.avatar_hash);
        self.toast.success(response.detail);
        self.get('options').setProperties(response.options);
        self.set('activeForm', 'select-avatar-type-form');
      }, function(jqXHR) {
        if (self.isDestroyed) { return; }
        if (jqXHR.status === 400) {
          self.toast.error(jqXHR.responseJSON.detail);
        } else {
          self.toast.apiError(jqXHR);
        }
      }).finally(function() {
        if (self.isDestroyed) { return; }
        self.setProperties({
          'isBusy': false,
          'activeItem': null
        });
      });
    },

    cancel: function() {
      this.set('activeForm', 'select-avatar-type-form');
    }
  }
});
