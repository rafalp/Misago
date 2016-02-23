import React from 'react'; // jshint ignore:line
import Followers from 'misago/components/profile/followers';

export default class extends Followers {
  setSpecialProps() {
    this.PRELOADED_DATA_KEY = 'PROFILE_FOLLOWS';
    this.TITLE = gettext('Follows');
    this.API_FILTER = 'follows';
  }

  getLabel() {
    if (!this.state.isLoaded) {
      return gettext('Loading...');
    } else if (this.state.search) {
      let message = ngettext(
        "Found %(users)s user.",
        "Found %(users)s users.",
        this.state.count);

      return interpolate(message, {
        'users': this.state.count
      }, true);
    } else if (this.props.profile.id === this.props.user.id) {
      let message = ngettext(
        "You are following %(users)s user.",
        "You are following %(users)s users.",
        this.state.count);

      return interpolate(message, {
        'users': this.state.count
      }, true);
    } else {
      let message = ngettext(
        "%(username)s is following %(users)s user.",
        "%(username)s is following %(users)s users.",
        this.state.count);

      return interpolate(message, {
        'username': this.props.profile.username,
        'users': this.state.count
      }, true);
    }
  }

  getEmptyMessage() {
    if (this.state.search) {
      return gettext("Search returned no users matching specified criteria.");
    } else if (this.props.user.id === this.props.profile.id) {
      return gettext("You are not following any users.");
    } else {
      return interpolate(gettext("%(username)s is not following any users."), {
        'username': this.props.profile.username
      }, true);
    }
  }
}