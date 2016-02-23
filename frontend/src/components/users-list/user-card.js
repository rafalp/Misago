import React from 'react';
import Avatar from 'misago/components/avatar'; // jshint ignore:line
import Status, { StatusIcon, StatusLabel } from 'misago/components/user-status'; // jshint ignore:line

export default class extends React.Component {
  getClassName() {
    if (this.props.user.rank.css_class) {
      return 'user-card user-card-' + this.props.user.rank.css_class + ' ui-ready';
    } else {
      return 'user-card ui-ready';
    }
  }

  getUserStatus() {
    if (this.props.showStatus) {
      if (this.props.user.status) {
        /* jshint ignore:start */
        return <Status user={this.props.user} status={this.props.user.status}>
          <StatusIcon user={this.props.user}
                      status={this.props.user.status} />
          <StatusLabel user={this.props.user}
                       status={this.props.user.status}
                       className="status-label" />
        </Status>;
        /* jshint ignore:end */
      } else {
        /* jshint ignore:start */
        return <span className="user-status">
          <span className="status-icon ui-preview">
            &nbsp;
          </span>
          <span className="status-label ui-preview">
            &nbsp;
          </span>
        </span>;
        /* jshint ignore:end */
      }
    } else {
      return null;
    }
  }

  getUserTitle() {
    if (this.props.user.title) {
      /* jshint ignore:start */
      return <span className="user-title">{this.props.user.title}</span>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getUserJoinedOn() {
    /* jshint ignore:start */
    let title = interpolate(gettext("Joined on %(joined_on)s"), {
      'joined_on': this.props.user.joined_on.format('LL, LT')
    }, true);

    let age = interpolate(gettext("Joined %(joined_on)s"), {
      'joined_on': this.props.user.joined_on.fromNow()
    }, true);

    return <span className="user-joined-on" title={title}>
      {age}
    </span>;
    /* jshint ignore:end */
  }

  render() {
    /* jshint ignore:start */
    return <div className={this.getClassName()}>
      <div className="user-card-bg-image">
        <Avatar user={this.props.user} size="400" className="bg-image" />

        <div className="user-card-bg">
          <div className="user-details">

            <div className="user-avatar">
              <a href={this.props.user.absolute_url}>
                <Avatar user={this.props.user} size="400" />
              </a>
            </div>

            <h4 className="user-name">
              <a href={this.props.user.absolute_url} className="item-title">
                {this.props.user.username}
              </a>
            </h4>

            <p className="user-subscript">
              {this.getUserStatus()}
              {this.getUserTitle()}
              {this.getUserJoinedOn()}
            </p>

          </div>
          <div className="user-card-stats">

            <ul className="list-unstyled">
              <li className="user-posts-count">
                <strong>{this.props.user.posts}</strong>
                <small>{gettext("posts")}</small>
              </li>
              <li className="user-threads-count">
                <strong>{this.props.user.threads}</strong>
                <small>{gettext("threads")}</small>
              </li>
              <li className="user-followers-count">
                <strong>{this.props.user.followers}</strong>
                <small>{gettext("followers")}</small>
              </li>
            </ul>

          </div>
        </div>
      </div>
    </div>;
    /* jshint ignore:end */
  }
}