import Ember from 'ember';

export default Ember.Component.extend({
  classNames: 'user-state',
  classNameBindings: [
    'user.state.is_banned:user-banned',
    'user.state.is_hidden:user-hidden',
    'user.state.is_online_hidden:user-online',
    'user.state.is_offline_hidden:user-offline',
    'user.state.is_online:user-online',
    'user.state.is_offline:user-offline'
  ],

  attributeBindings: ['title'],

  title: function() {
    if (this.get('user.state.is_banned')) {
      if (this.get('user.state.banned_until')) {
        return interpolate(gettext('%(username)s\'s is banned until %(ban_expires)s.'), {
            'username': this.get('user.username'),
            'ban_expires': moment(this.get('user.state.banned_until')).format('LL, LT')
          }, true);
      } else {
        return interpolate(gettext('%(username)s\'s is banned.'), {
            'username': this.get('user.username')
          }, true);
      }

    } else if (this.get('user.state.is_hidden')) {
      return interpolate(gettext('%(username)s\'s activity is hidden.'), {
          'username': this.get('user.username')
        }, true);

    } else if (this.get('user.state.is_online_hidden')) {
      return interpolate(gettext('%(username)s is online and hidden.'), {
          'username': this.get('user.username')
        }, true);

    } else if (this.get('user.state.is_offline_hidden')) {
      return interpolate(gettext('%(username)s was last seen hidden %(last_click)s.'), {
          'username': this.get('user.username'),
          'last_click': this.get('lastClick').fromNow()
        }, true);

    } else if (this.get('user.state.is_online')) {
      return interpolate(gettext('%(username)s is online.'), {
          'username': this.get('user.username')
        }, true);

    } else if (this.get('user.state.is_offline')) {
      return interpolate(gettext('%(username)s was last seen %(last_click)s.'), {
          'username': this.get('user.username'),
          'last_click': this.get('lastClick').fromNow()
        }, true);
    }
  }.property(
    'user.state.is_banned',
    'user.state.is_hidden',
    'user.state.is_online_hidden',
    'user.state.is_offline_hidden',
    'user.state.is_online',
    'user.state.is_offline',
    'user.state.banned_until',
    'lastClick'
  ),

  lastClick: function() {
    return moment(this.get('user.state.last_click'));
  }.property('user.state.last_click', 'clock.tick')
});
