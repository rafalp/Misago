import React from 'react';
import Avatar from 'misago/components/avatar'; // jshint ignore:line
import FollowButton from 'misago/components/profile/follow-button'; // jshint ignore:line
import ModerationNav from 'misago/components/profile/moderation/nav'; // jshint ignore:line
import Status, { StatusIcon, StatusLabel } from 'misago/components/user-status'; // jshint ignore:line

export default class extends React.Component {
  getUserStatus() {
    /* jshint ignore:start */
    return <li className="user-status-display">
      <Status user={this.props.profile} status={this.props.profile.status}>
        <StatusIcon user={this.props.profile}
                    status={this.props.profile.status} />
        <StatusLabel user={this.props.profile}
                     status={this.props.profile.status}
                     className="status-label" />
      </Status>
    </li>;
    /* jshint ignore:end */
  }

  getUserRank() {
    if (this.props.profile.rank.is_tab) {
      /* jshint ignore:start */
      return <li className="user-rank">
        <a href={this.props.profile.rank.absolute_url} className="item-title">
          {this.props.profile.rank.name}
        </a>
      </li>;
      /* jshint ignore:end */
    } else {
      /* jshint ignore:start */
      return <li className="user-rank">
        <span className="item-title">{this.props.profile.rank.name}</span>
      </li>;
      /* jshint ignore:end */
    }
  }

  getUserTitle() {
    if (this.props.profile.title) {
      /* jshint ignore:start */
      return <li className="user-title">
        {this.props.profile.title}
      </li>;
      /* jshint ignore:end */
    } else if (this.props.profile.rank.title) {
      /* jshint ignore:start */
      return <li className="user-title">
        {this.props.profile.rank.title}
      </li>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getJoinedOn() {
    /* jshint ignore:start */
    let title = interpolate(gettext("Joined on %(joined_on)s"), {
      'joined_on': this.props.profile.joined_on.format('LL, LT')
    }, true);

    let age = interpolate(gettext("Joined %(joined_on)s"), {
      'joined_on': this.props.profile.joined_on.fromNow()
    }, true);

    return <li className="user-joined-on">
      <abbr title={title}>
        {age}
      </abbr>
    </li>;
    /* jshint ignore:end */
  }

  getEmail() {
    if (this.props.profile.email) {
      /* jshint ignore:start */
      return <li className="user-email">
        <a href={'mailto:' + this.props.profile.email} className="item-title">
          {this.props.profile.email}
        </a>
      </li>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getFollowButton() {
    if (this.props.profile.acl.can_follow) {
      /* jshint ignore:start */
      return <FollowButton className="btn btn-aligned hidden-xs hidden-sm"
                           profile={this.props.profile} />;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getModerationButton() {
    if (this.props.profile.acl.can_moderate) {
      /* jshint ignore:start */
      return <div className="btn-group btn-aligned hidden-xs hidden-sm">
        <button className="btn btn-default btn-moderate dropdown-toggle"
                type="button"
                data-toggle="dropdown"
                aria-haspopup="true"
                aria-expanded="false">
          <span className="material-icon">
            tonality
          </span>
          {gettext("Moderation")}
        </button>
        <ModerationNav profile={this.props.profile} />
      </div>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  render() {
    /* jshint ignore:start */
    return<div className="page-header">
      <div className="container">

        <div className="row">
          <div className="col-md-9 col-md-offset-3">

            <h1 className="pull-left">
              <Avatar user={this.props.profile} size="100" />
              <span className="user-name">{this.props.profile.username}</span>
            </h1>

            {this.getFollowButton()}
            {this.getModerationButton()}

            <button className="btn btn-default btn-aligned btn-icon btn-dropdown-toggle hidden-md hidden-lg"
                    type="button"
                    onClick={this.props.toggleNav}
                    aria-haspopup="true"
                    aria-expanded={this.props.dropdown ? 'true' : 'false'}>
              <i className="material-icon">
                menu
              </i>
            </button>

          </div>
        </div>

      </div>
      <div className="header-stats">
        <div className="container">
          <div className="row">
            <div className="col-md-9 col-md-offset-3">

              <ul className="list-inline">
                {this.getUserStatus()}
                {this.getUserRank()}
                {this.getUserTitle()}
                {this.getJoinedOn()}
                {this.getEmail()}
              </ul>

            </div>
          </div>
        </div>
      </div>
    </div>;
    /* jshint ignore:end */
  }
}