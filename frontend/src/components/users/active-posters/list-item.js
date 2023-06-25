import React from "react"
import { Link } from "react-router"
import Avatar from "misago/components/avatar"
import Status, { StatusIcon, StatusLabel } from "misago/components/user-status"
import misago from "misago/index"
import * as random from "misago/utils/random"

export default class extends React.Component {
  getClassName() {
    if (this.props.rank.css_class) {
      return "list-group-item list-group-rank-" + this.props.rank.css_class
    } else {
      return "list-group-item"
    }
  }

  getUserStatus() {
    if (this.props.user.status) {
      return (
        <Status user={this.props.user} status={this.props.user.status}>
          <StatusIcon user={this.props.user} status={this.props.user.status} />
          <StatusLabel
            user={this.props.user}
            status={this.props.user.status}
            className="status-label hidden-xs hidden-sm"
          />
        </Status>
      )
    }

    return (
      <span className="user-status">
        <span className="status-icon ui-preview-text">&nbsp;</span>
        <span
          className="status-label ui-preview-text hidden-xs hidden-sm"
          style={{ width: random.int(30, 50) + "px" }}
        >
          &nbsp;
        </span>
      </span>
    )
  }

  getRankName() {
    if (!this.props.rank.is_tab) {
      return (
        <span className="rank-name item-title">{this.props.rank.name}</span>
      )
    }

    let rankUrl = misago.get("USERS_LIST_URL") + this.props.rank.slug + "/"
    return (
      <Link to={rankUrl} className="rank-name item-title">
        {this.props.rank.name}
      </Link>
    )
  }

  getUserTitle() {
    if (!this.props.user.title) return null

    return (
      <span className="user-title hidden-xs hidden-sm">
        {this.props.user.title}
      </span>
    )
  }

  render() {
    return (
      <li className={this.getClassName()}>
        <div className="rank-user-avatar">
          <a href={this.props.user.url}>
            <Avatar user={this.props.user} size={50} size2x={64} />
          </a>
        </div>

        <div className="rank-user">
          <div className="user-name">
            <a href={this.props.user.url} className="item-title">
              {this.props.user.username}
            </a>
          </div>
          <div className="user-details">
            {this.getUserStatus()}
            {this.getRankName()}
            {this.getUserTitle()}
          </div>
          <div className="user-compact-stats visible-xs-block">
            <span className="rank-position">
              <strong>#{this.props.counter}</strong>
              <small>{pgettext("top posters list item", "Rank")}</small>
            </span>

            <span className="rank-posts-counted">
              <strong>{this.props.user.meta.score}</strong>
              <small>{pgettext("top posters list item", "Ranked posts")}</small>
            </span>
          </div>
        </div>

        <div className="rank-position hidden-xs">
          <strong>#{this.props.counter}</strong>
          <small>{pgettext("top posters list item", "Rank")}</small>
        </div>

        <div className="rank-posts-counted hidden-xs">
          <strong>{this.props.user.meta.score}</strong>
          <small>{pgettext("top posters list item", "Ranked posts")}</small>
        </div>

        <div className="rank-posts-total hidden-xs">
          <strong>{this.props.user.posts}</strong>
          <small>{pgettext("top posters list item", "Total posts")}</small>
        </div>
      </li>
    )
  }
}
