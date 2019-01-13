import React from "react"
import Avatar from "misago/components/avatar"

export default class extends React.Component {
  renderUserAvatar() {
    if (this.props.change.changed_by) {
      return (
        <a
          href={this.props.change.changed_by.url}
          className="user-avatar-wrapper"
        >
          <Avatar user={this.props.change.changed_by} size="100" />
        </a>
      )
    } else {
      return (
        <span className="user-avatar-wrapper">
          <Avatar size="100" />
        </span>
      )
    }
  }

  renderUsername() {
    if (this.props.change.changed_by) {
      return (
        <a href={this.props.change.changed_by.url} className="item-title">
          {this.props.change.changed_by.username}
        </a>
      )
    } else {
      return (
        <span className="item-title">
          {this.props.change.changed_by_username}
        </span>
      )
    }
  }

  render() {
    return (
      <li className="list-group-item" key={this.props.change.id}>
        <div className="change-avatar">{this.renderUserAvatar()}</div>
        <div className="change-author">{this.renderUsername()}</div>
        <div className="change">
          <span className="old-username">{this.props.change.old_username}</span>
          <span className="material-icon">arrow_forward</span>
          <span className="new-username">{this.props.change.new_username}</span>
        </div>
        <div className="change-date">
          <abbr title={this.props.change.changed_on.format("LLL")}>
            {this.props.change.changed_on.fromNow()}
          </abbr>
        </div>
      </li>
    )
  }
}
