import React from 'react';
import Avatar from 'misago/components/avatar'; // jshint ignore:line
import Status, { StatusIcon, StatusLabel } from 'misago/components/user-status'; // jshint ignore:line
import * as random from 'misago/utils/random'; // jshint ignore:line

export default class extends React.Component {
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
          <span className="status-icon ui-preview-text">
            &nbsp;
          </span>
          <span className="status-label ui-preview-text"
                style={{width: random.int(30, 50) + "px"}}>
            &nbsp;
          </span>
        </span>;
        /* jshint ignore:end */
      }
    } else {
      return null;
    }
  }

  getRankName() {
    if (this.props.showRank) {
      if (this.props.user.rank.is_tab) {
        /* jshint ignore:start */
        return <a href={this.props.user.rank.absolute_url}
                  className="item-title rank-name">
          {this.props.user.rank.name}
        </a>;
        /* jshint ignore:end */
      } else {
        /* jshint ignore:start */
        return <span className="item-title rank-name">
          {this.props.user.rank.name}
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

  getPostsCount() {
    let message = ngettext(
      "%(posts)s post",
      "%(posts)s posts",
      this.props.user.posts);

    return interpolate(message, {
      'posts': this.props.user.posts
    }, true);
  }

  getThreadsCount() {
    let message = ngettext(
      "%(threads)s thread",
      "%(threads)s threads",
      this.props.user.threads);

    return interpolate(message, {
      'threads': this.props.user.threads
    }, true);
  }

  getFollowersCount() {
    let message = ngettext(
      "%(followers)s follower",
      "%(followers)s followers",
      this.props.user.followers);

    return interpolate(message, {
      'followers': this.props.user.followers
    }, true);
  }

  getClassName() {
    if (this.props.user.rank.css_class) {
      return 'user-card user-card-' + this.props.user.rank.css_class + ' ui-ready';
    } else {
      return 'user-card ui-ready';
    }
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
              {this.getRankName()}
              {this.getUserTitle()}
              {this.getUserJoinedOn()}
            </p>

          </div>
          <div className="user-card-stats">

            <ul className="list-unstyled">
              <li className="user-posts-count">
                {this.getPostsCount()}
              </li>
              <li className="user-threads-count">
                {this.getThreadsCount()}
              </li>
              <li className="user-followers-count">
                {this.getFollowersCount()}
              </li>
            </ul>

          </div>
        </div>
      </div>
    </div>;
    /* jshint ignore:end */
  }
}