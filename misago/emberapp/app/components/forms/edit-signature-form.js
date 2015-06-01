import Ember from 'ember';

export default Ember.Component.extend({
  tagName: 'form',

  isLoaded: false,
  isSaving: false,
  isErrored: false,

  options: null,
  signature: '',

  apiUrl: function() {
    return 'users/' + this.auth.get('user.id') + '/signature';
  }.property(),

  loadOptions: function() {
    var self = this;
    this.ajax.get(this.get('apiUrl')
    ).then(function(options) {
      if (self.isDestroyed) { return; }
      self.setProperties({
        'options': Ember.Object.create(options),
        'signature': self.get('options.signature.plain') || '',
        'isLoaded': true
      });
    }, function(jqXHR) {
      if (self.isDestroyed) { return; }
      if (typeof jqXHR.responseJSON !== 'undefined') {
        self.set('isErrored', jqXHR.responseJSON);
      } else if (jqXHR.status === 0) {
        self.set('isErrored', {'detail': gettext('Lost connection with application.')});
      } else {
        self.set('isErrored', {'detail': gettext('Application has errored.')});
      }
    });
  }.on('init'),

  submit: function() {
    if (this.get('isSaving')) {
      return false;
    }

    if (this.get('signature').length > this.get('options.limit')) {
      this.toast.warning(gettext('Signature is too long.'));
      return false;
    }

    this.set('isSaving', true);

    var self = this;
    this.ajax.post(this.get('apiUrl'), {'signature': this.get('signature')}
    ).then(function(response) {
      if (self.isDestroyed) { return; }
      self.success(response);
    }, function(jqXHR) {
      if (self.isDestroyed) { return; }
      self.error(jqXHR);
    }).finally(function() {
      if (self.isDestroyed) { return; }
      self.set('isSaving', false);
    });

    return false;
  },

  success: function(responseJSON) {
    this.get('options').setProperties(responseJSON);
    if (this.get('options.signature.plain')) {
      this.toast.success(gettext('Your signature was updated.'));
    } else {
      this.toast.info(gettext('Your signature was cleared.'));
    }
  },

  error: function(jqXHR) {
    if (jqXHR.status === 400) {
      this.toast.error(jqXHR.responseJSON.detail);
    } else {
      this.toast.apiError(jqXHR);
    }
  }
});
