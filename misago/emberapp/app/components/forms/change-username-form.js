import Ember from 'ember';

export default Ember.Component.extend({
  tagName: 'form',
  classNames: 'form-horizontal',

  isLoaded: false,
  loadError: null,
  isBusy: false,

  options: null,
  username: '',

  validation: null,
  setValidation: function() {
    this.set('validation', Ember.Object.create({}));
  }.on('init'),

  apiUrl: function() {
    return 'users/' + this.auth.get('user.id') + '/username';
  }.property(),

  loadOptions: function() {
    var self = this;
    this.ajax.get(this.get('apiUrl')
    ).then(function(options) {
      if (self.isDestroyed) { return; }
      self.setProperties({
        'options': Ember.Object.create(options),
        'isLoaded': true
      });
    }, function(jqXHR) {
      if (self.isDestroyed) { return; }
      if (typeof jqXHR.responseJSON !== 'undefined') {
        self.set('loadError', jqXHR.responseJSON);
      } else if (jqXHR.status === 0) {
        self.set('loadError', {'detail': gettext('Lost connection with application.')});
      } else {
        self.set('loadError', {'detail': gettext('Application has errored.')});
      }
    });
  }.on('init'),

  usernameValidation: function() {
    var state = true;

    var value = Ember.$.trim(this.get('username'));
    var valueLength = value.length;

    var limit = 0;
    var message = null;
    if (valueLength < this.get('options.length_min')) {
      limit = this.get('options.length_min');
      message = ngettext('Username must be at least %(limit)s character long.',
                         'Username must be at least %(limit)s characters long.',
                         limit);
      state = [interpolate(message, {limit: limit}, true)];
    } else if (valueLength > this.get('options.length_max')) {
      limit = this.get('options.length_max');
      message = ngettext('Username cannot be longer than %(limit)s characters.',
                         'Username cannot be longer than %(limit)s characters.',
                         limit);
      state = [interpolate(message, {limit: limit}, true)];
    } else if (!new RegExp('^[0-9a-z]+$', 'i').test(value)) {
      state = [gettext('Username can only contain latin alphabet letters and digits.')];
    } else if (value === this.get('auth.user.username')) {
      state = [gettext('New username is same as current one.')];
    }

    if (state === true) {
      this.set('validation.username', 'ok');
    } else {
      this.set('validation.username', state);
    }
  }.observes('username'),

  submit: function() {
    if (this.get('isBusy')) {
      return false;
    }

    var data = {
      username: Ember.$.trim(this.get('username')),
    };

    if (data.username.length === 0) {
      this.toast.error(gettext('Enter new username.'));
      return false;
    }

    if (this.$('.has-error').length) {
      this.toast.error(gettext('Form contains errors.'));
      return false;
    }

    this.set('isBusy', true);

    var self = this;
    this.ajax.post(this.get('apiUrl'), data
    ).then(function(response) {
      if (self.isDestroyed) { return; }
      self.success(response);
    }, function(jqXHR) {
      if (self.isDestroyed) { return; }
      self.error(jqXHR);
    }).finally(function() {
      if (self.isDestroyed) { return; }
      self.set('isBusy', false);
    });

    return false;
  },

  success: function(responseJSON) {
    this.set('username', '');
    this.set('validation', Ember.Object.create({}));

    this.toast.success(gettext('Your username has been changed.'));
    this.get('options').setProperties(responseJSON.options);

    var oldUsername = this.get('auth.user.username');

    this.get('auth.user').setProperties({
      'username': responseJSON.username,
      'slug': responseJSON.slug
    });

    var userPOJO = this.auth.getUserPOJO();

    this.store.pushPayload({
      'username-changes': [
        {
          'id': Math.floor(new Date().getTime() / 1000),
          'user': userPOJO,
          'changed_by': userPOJO,
          'changed_by_username': this.get('auth.user.username'),
          'changed_by_slug': this.get('auth.user.slug'),
          'changed_on': moment(),
          'new_username': this.get('auth.user.username'),
          'old_username': oldUsername
        }
      ]
    });
  },

  error: function(jqXHR) {
    var rejection = jqXHR.responseJSON;
    if (jqXHR.status === 400) {
      this.toast.error(rejection.detail);
      this.get('options').setProperties(rejection.options);
    } else {
      this.toast.apiError(jqXHR);
    }
  },

  changesLeft: Ember.computed.alias('options.changes_left'),

  changesLeftMessage: function() {
    var changes = this.get('options.changes_left');
    var message = ngettext('You can change your username %(changes)s more time.',
                           'You can change your username %(changes)s more times.',
                           changes);
    return interpolate(message, {changes: changes}, true);
  }.property('options.changes_left'),

  nextChange: function() {
    if (this.get('options.next_on')) {
      return moment(this.get('options.next_on'));
    } else {
      return null;
    }
  }.property('options.next_on', 'clock.tick')
});
