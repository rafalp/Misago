import React from 'react';

export default class extends React.Component {
  getClass() {
    return getStatusClassName(this.props.status);
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
    return <span className="material-icon status-icon">
      {this.getIcon()}
    </span>;
    /* jshint ignore:end */
  }

}

export class StatusLabel extends React.Component {
  getHelp() {
    return getStatusDescription(this.props.user, this.props.status);
  }

  getLabel() {
    if (this.props.status.is_banned) {
      return gettext("Banned");
    } else if (this.props.status.is_hidden) {
      return gettext("Hidden");
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

export function getStatusClassName(status) {
  let className = '';
  if (status.is_banned) {
    className = 'banned';
  } else if (status.is_hidden) {
    className = 'offline';
  } else if (status.is_online_hidden) {
    className = 'online';
  } else if (status.is_offline_hidden) {
    className = 'offline';
  } else if (status.is_online) {
    className = 'online';
  } else if (status.is_offline) {
    className = 'offline';
  }

  return 'user-status user-' + className;
}

export function getStatusDescription(user, status) {
  if (status.is_banned) {
    if (status.banned_until) {
      return interpolate(gettext("%(username)s is banned until %(ban_expires)s"), {
        username: user.username,
        ban_expires: status.banned_until.format('LL, LT')
      }, true);
    } else {
      return interpolate(gettext("%(username)s is banned"), {
        username: user.username
      }, true);
    }
  } else if (status.is_hidden) {
    return interpolate(gettext("%(username)s is hiding presence"), {
      username: user.username
    }, true);
  } else if (status.is_online_hidden) {
    return interpolate(gettext("%(username)s is online (hidden)"), {
      username: user.username
    }, true);
  } else if (status.is_offline_hidden) {
    return interpolate(gettext("%(username)s was last seen %(last_click)s (hidden)"), {
      username: user.username,
      last_click: status.last_click.fromNow()
    }, true);
  } else if (status.is_online) {
    return interpolate(gettext("%(username)s is online"), {
      username: user.username
    }, true);
  } else if (status.is_offline) {
    return interpolate(gettext("%(username)s was last seen %(last_click)s"), {
      username: user.username,
      last_click: status.last_click.fromNow()
    }, true);
  }
}