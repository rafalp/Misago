import React from "react"

export default class extends React.Component {
  getClass() {
    return getStatusClassName(this.props.status)
  }

  render() {
    return <span className={this.getClass()}>{this.props.children}</span>
  }
}

export class StatusIcon extends React.Component {
  getIcon() {
    if (this.props.status.is_banned) {
      return "remove_circle_outline"
    } else if (this.props.status.is_hidden) {
      return "help_outline"
    } else if (this.props.status.is_online_hidden) {
      return "label"
    } else if (this.props.status.is_offline_hidden) {
      return "label_outline"
    } else if (this.props.status.is_online) {
      return "lens"
    } else if (this.props.status.is_offline) {
      return "panorama_fish_eye"
    }
  }

  render() {
    return <span className="material-icon status-icon">{this.getIcon()}</span>
  }
}

export class StatusLabel extends React.Component {
  getHelp() {
    return getStatusDescription(this.props.user, this.props.status)
  }

  getLabel() {
    if (this.props.status.is_banned) {
      return pgettext("user status", "Banned")
    } else if (this.props.status.is_hidden) {
      return pgettext("user status", "Hidden")
    } else if (this.props.status.is_online_hidden) {
      return pgettext("user status", "Online (hidden)")
    } else if (this.props.status.is_offline_hidden) {
      return pgettext("user status", "Offline (hidden)")
    } else if (this.props.status.is_online) {
      return pgettext("user status", "Online")
    } else if (this.props.status.is_offline) {
      return pgettext("user status", "Offline")
    }
  }

  render() {
    return (
      <span
        className={this.props.className || "status-label"}
        title={this.getHelp()}
      >
        {this.getLabel()}
      </span>
    )
  }
}

export function getStatusClassName(status) {
  let className = ""
  if (status.is_banned) {
    className = "banned"
  } else if (status.is_hidden) {
    className = "offline"
  } else if (status.is_online_hidden) {
    className = "online"
  } else if (status.is_offline_hidden) {
    className = "offline"
  } else if (status.is_online) {
    className = "online"
  } else if (status.is_offline) {
    className = "offline"
  }

  return "user-status user-" + className
}

export function getStatusDescription(user, status) {
  if (status.is_banned) {
    if (status.banned_until) {
      return interpolate(
        pgettext("user status", "%(username)s is banned until %(ban_expires)s"),
        {
          username: user.username,
          ban_expires: status.banned_until.format("LL, LT"),
        },
        true
      )
    } else {
      return interpolate(
        pgettext("user status", "%(username)s is banned"),
        {
          username: user.username,
        },
        true
      )
    }
  } else if (status.is_hidden) {
    return interpolate(
      pgettext("user status", "%(username)s is hiding presence"),
      {
        username: user.username,
      },
      true
    )
  } else if (status.is_online_hidden) {
    return interpolate(
      pgettext("user status", "%(username)s is online (hidden)"),
      {
        username: user.username,
      },
      true
    )
  } else if (status.is_offline_hidden) {
    return interpolate(
      pgettext(
        "user status",
        "%(username)s was last seen %(last_click)s (hidden)"
      ),
      {
        username: user.username,
        last_click: status.last_click.fromNow(),
      },
      true
    )
  } else if (status.is_online) {
    return interpolate(
      pgettext("user status", "%(username)s is online"),
      {
        username: user.username,
      },
      true
    )
  } else if (status.is_offline) {
    return interpolate(
      pgettext("user status", "%(username)s was last seen %(last_click)s"),
      {
        username: user.username,
        last_click: status.last_click.fromNow(),
      },
      true
    )
  }
}
