import Ember from 'ember';

export default Ember.Component.extend({
  tagName: 'form',
  classNames: 'form-horizontal',

  isBusy: false,

  subscribeToChoices: [
    {value: 0, label: gettext('No')},
    {value: 1, label: gettext('Bookmark')},
    {value: 2, label: gettext('Bookmark with e-mail notification')}
  ],

  privateThreadInvitesChoices: [
    {value: 0, label: gettext('Everybody')},
    {value: 1, label: gettext('Users I follow')},
    {value: 2, label: gettext('Nobody')}
  ],

  is_hiding_presence: null,
  limits_private_thread_invites_to: null,
  subscribe_to_started_threads: null,
  subscribe_to_replied_threads: null,

  setInitialValues: function() {
    this.setProperties({
      is_hiding_presence: this.get('auth.user.is_hiding_presence'),
      limits_private_thread_invites_to: this.get('auth.user.limits_private_thread_invites_to'),
      subscribe_to_started_threads: this.get('auth.user.subscribe_to_started_threads'),
      subscribe_to_replied_threads: this.get('auth.user.subscribe_to_replied_threads'),
    });
  }.on('init'),

  validation: null,
  setValidation: function() {
    this.set('validation', Ember.Object.create({}));
  }.on('init'),

  isHidingPresenceValidation: function() {
    this.set('validation.is_hiding_presence', undefined);
  }.observes('is_hiding_presence'),

  limitsPrivateThreadInvitesToValidation: function() {
    this.set('validation.limits_private_thread_invites_to', undefined);
  }.observes('limits_private_thread_invites_to'),

  subscribeToStartedThreadsValidation: function() {
    this.set('validation.subscribe_to_started_threads', undefined);
  }.observes('subscribe_to_started_threads'),

  subscribeToRepliedThreadsValidation: function() {
    this.set('validation.subscribe_to_replied_threads', undefined);
  }.observes('subscribe_to_replied_threads'),

  apiUrl: function() {
    return 'users/' + this.auth.get('user.id') + '/forum-options';
  }.property(),

  submit: function() {
    if (this.get('isBusy')) {
      return false;
    }

    var newOptions = {
      is_hiding_presence: this.get('is_hiding_presence'),
      limits_private_thread_invites_to: this.get('limits_private_thread_invites_to'),
      subscribe_to_started_threads: this.get('subscribe_to_started_threads'),
      subscribe_to_replied_threads: this.get('subscribe_to_replied_threads')
    };

    this.set('isBusy', true);

    var self = this;
    this.ajax.post(this.get('apiUrl'), newOptions
    ).then(function(response) {
      if (self.isDestroyed) { return; }
      self.success(response, newOptions);
    }, function(jqXHR) {
      if (self.isDestroyed) { return; }
      self.error(jqXHR);
    }).finally(function() {
      if (self.isDestroyed) { return; }
      self.set('isBusy', false);
    });

    return false;
  },

  success: function(responseJSON, newOptions) {
    this.get('auth.user').setProperties(newOptions);
    this.toast.success(responseJSON.detail);
  },

  error: function(jqXHR) {
    if (jqXHR.status === 400) {
      this.toast.error(gettext("Form contains errors."));
      this.get('validation').setProperties(jqXHR.responseJSON);
    } else {
      this.toast.apiError(jqXHR);
    }
  }
});
