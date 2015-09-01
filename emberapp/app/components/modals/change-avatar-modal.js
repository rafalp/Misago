import Ember from 'ember';
import ModalComponent from 'misago/mixins/modal-component';

export default Ember.Component.extend(ModalComponent, {
  className: 'modal-change-avatar',

  isLoaded: false,
  loadError: false,

  options: null,

  loadOptions: function() {
    var self = this;
    this.ajax.get('users/' + this.auth.get('user.id') + '/avatar'
    ).then(function(options) {
      if (self.isDestroyed) { return; }
      self.set('options', Ember.Object.create(options));
      self.set('isLoaded', true);
    }, function(jqXHR) {
      if (self.isDestroyed) { return; }
      if (typeof jqXHR.responseJSON !== 'undefined') {
        self.set('loadError', jqXHR.responseJSON);
      } else if (jqXHR.status === 0) {
        self.set('loadError', {detail: gettext('Lost connection with application.')});
      } else {
        self.set('loadError', {detail: gettext('Application has errored.')});
      }
    });
  }.on('didInsertElement'),

  // Page control

  activeForm: 'select-avatar-type-form'
});
