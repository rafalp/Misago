import React from 'react';

export default class extends React.Component {
  getClass() {
    let status = '';
    if (this.props.status.is_banned) {
      status = 'banned';
    } else if (this.props.status.is_hidden) {
      status = 'offline';
    } else if (this.props.status.is_online_hidden) {
      status = 'online';
    } else if (this.props.status.is_offline_hidden) {
      status = 'offline';
    } else if (this.props.status.is_online) {
      status = 'online';
    } else if (this.props.status.is_offline) {
      status = 'offline';
    }

    return 'user-status user-' + status;
  }

  render() {
    /* jshint ignore:start */
    return <span className={this.getClass()}>
      {this.props.children}
    </span>;
    /* jshint ignore:end */
  }
}

export class StatusIcon extends React.Component {
  getIcon() {
    if (this.props.status.is_banned) {
      return 'remove_circle_outline';
    } else if (this.props.status.is_hidden) {
      return 'help_outline';
    } else if (this.props.status.is_online_hidden) {
      return 'label';
    } else if (this.props.status.is_offline_hidden) {
      return 'label_outline';
    } else if (this.props.status.is_online) {
      return 'lens';
    } else if (this.props.status.is_offline) {
      return 'panorama_fish_eye';
    }
  }

  render() {
    /* jshint ignore:start */
    return <span className="status-icon">
      {this.getIcon()}
    </span>;
    /* jshint ignore:end */
  }

}

export class StatusLabel extends React.Component {
  getHelp() {
    if (this.props.status.is_banned) {
      if (this.props.status.banned_until) {
        return interpolate(gettext("%(username)s is hiding banned until %(ban_expires)s"), {
          username: this.props.user.username,
          ban_expires: this.props.status.banned_until.format('LL, LT')
        }, true);
      } else {
        return interpolate(gettext("%(username)s is hiding banned"), {
          username: this.props.user.username
        }, true);
      }
    } else if (this.props.status.is_hidden) {
      return interpolate(gettext("%(username)s is hiding activity"), {
        username: this.props.user.username
      }, true);
    } else if (this.props.status.is_online_hidden) {
      return interpolate(gettext("%(username)s is online (hidden)"), {
        username: this.props.user.username
      }, true);
    } else if (this.props.status.is_offline_hidden) {
      return interpolate(gettext("%(username)s was last seen %(last_click)s (hidden)"), {
        username: this.props.user.username,
        last_click: this.props.state.lastClick.fromNow()
      }, true);
    } else if (this.props.status.is_online) {
      return interpolate(gettext("%(username)s is online"), {
        username: this.props.user.username
      }, true);
    } else if (this.props.status.is_offline) {
      return interpolate(gettext("%(username)s was last seen %(last_click)s"), {
        username: this.props.user.username,
        last_click: this.props.state.lastClick.fromNow()
      }, true);
    }
  }

  getLabel() {
    if (this.props.status.is_banned) {
      return gettext("Banned");
    } else if (this.props.status.is_hidden) {
      return gettext("Hiding activity");
    } else if (this.props.status.is_online_hidden) {
      return gettext("Online (hidden)");
    } else if (this.props.status.is_offline_hidden) {
      return gettext("Offline (hidden)");
    } else if (this.props.status.is_online) {
      return gettext("Online");
    } else if (this.props.status.is_offline) {
      return gettext("Offline");
    }
  }

  render() {
    /* jshint ignore:start */
    return <span className={this.props.className || "status-label"}
                 title={this.getHelp()}>
      {this.getLabel()}
    </span>;
    /* jshint ignore:end */
  }
}