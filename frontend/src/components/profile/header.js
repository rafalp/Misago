import React from 'react';
import Avatar from 'misago/components/avatar'; // jshint ignore:line
import DropdownToggle from 'misago/components/dropdown-toggle'; // jshint ignore:line
import FollowButton from './follow-button'; // jshint ignore:line
import MessageButton from './message-button'; // jshint ignore:line
import ModerationNav from './moderation/nav'; // jshint ignore:line
import { CompactNav } from './navs'; // jshint ignore:line
import Status, { StatusIcon, StatusLabel } from 'misago/components/user-status'; // jshint ignore:line

export default class extends React.Component {
  getUserStatus() {
    /* jshint ignore:start */
    return (
      <li className="user-status-display">
        <Status
          user={this.props.profile}
          status={this.props.profile.status}
        >
          <StatusIcon
            user={this.props.profile}
            status={this.props.profile.status}
          />
          <StatusLabel
            user={this.props.profile}
            status={this.props.profile.status}
            className="status-label"
          />
        </Status>
      </li>
    );
    /* jshint ignore:end */
  }

  getUserRank() {
    if (this.props.profile.rank.is_tab) {
      /* jshint ignore:start */
      return (
        <li className="user-rank">
          <a href={this.props.profile.rank.url} className="item-title">
            {this.props.profile.rank.name}
          </a>
        </li>
      );
      /* jshint ignore:end */
    } else {
      /* jshint ignore:start */
      return (
        <li className="user-rank">
          <span className="item-title">{this.props.profile.rank.name}</span>
        </li>
      );
      /* jshint ignore:end */
    }
  }

  getUserTitle() {
    if (this.props.profile.title) {
      /* jshint ignore:start */
      return (
        <li className="user-title">
          {this.props.profile.title}
        </li>
      );
      /* jshint ignore:end */
    } else if (this.props.profile.rank.title) {
      /* jshint ignore:start */
      return (
        <li className="user-title">
          {this.props.profile.rank.title}
        </li>
      );
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

    return (
      <li className="user-joined-on">
        <abbr title={title}>
          {age}
        </abbr>
      </li>
    );
    /* jshint ignore:end */
  }

  getEmail() {
    if (this.props.profile.email) {
      /* jshint ignore:start */
      return (
        <li className="user-email">
          <a href={'mailto:' + this.props.profile.email} className="item-title">
            {this.props.profile.email}
          </a>
        </li>
      );
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getFollowButton() {
    if (this.props.profile.acl.can_follow) {
      /* jshint ignore:start */
      return (
        <FollowButton
          className="btn btn-block btn-outline"
          profile={this.props.profile}
        />
      );
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getModerationButton() {
    if (this.props.profile.acl.can_moderate) {
      /* jshint ignore:start */
      return (
        <div className="btn-group btn-group-justified">
          <div className="btn-group">
            <button
              className="btn btn-default btn-moderate btn-outline dropdown-toggle"
              type="button"
              data-toggle="dropdown"
              aria-haspopup="true"
              aria-expanded="false"
            >
              <span className="material-icon">
                tonality
              </span>
              {gettext("Moderation")}
            </button>
            <ModerationNav profile={this.props.profile} />
          </div>
        </div>
      );
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  render() {
    /* jshint ignore:start */
    const canFollow = this.props.profile.acl.can_follow;
    const canModerate = this.props.profile.acl.can_moderate;

    const isProfileOwner = this.props.user.id === this.props.profile.id;
    const canMessage = !isProfileOwner && this.props.user.acl.can_start_private_threads;

    let cols = 0;
    if (canFollow) cols += 1;
    if (canModerate) cols += 1;
    if (canMessage) cols += 1;

    const colsWidth = cols ? 2 * cols + 1 : 0;

    let headerClassName = 'page-header';
    if (this.props.profile.rank.css_class) {
      headerClassName += ' page-header-rank-' + this.props.profile.rank.css_class;
    }

    return (
      <div className="page-header-bg">
        <div className={headerClassName}>
          <div className="container">

            <IsDisabledMessage
              isActive={this.props.profile.is_active}
              requestedDelete={this.props.profile.delete_own_account}
            />

            <div className="row">
              <div className="col-md-9 col-md-offset-3">

                <div className="row">
                  <div className={"col-sm-" + (12 - colsWidth)}>

                    <Avatar
                      className="user-avatar user-avatar-sm"
                      user={this.props.profile}
                      size="100"
                      size2x="200"
                    />
                    <h1>{this.props.profile.username}</h1>

                  </div>
                  {!!cols && (
                    <div className={"col-sm-" + colsWidth}>

                      <div className="row xs-margin-top sm-margin-top">
                        {!!canMessage && (
                        <div className={getColStyle(cols, 0)}>
                          <MessageButton
                            className="btn btn-default btn-block btn-outline"
                            profile={this.props.profile}
                            user={this.props.user}
                          />
                        </div>
                        )}
                        {!!canFollow && (
                          <div className={getColStyle(cols, 1)}>
                            {this.getFollowButton()}
                          </div>
                        )}
                        {!!canModerate && (
                          <div className={getColStyle(cols, 2)}>
                            {this.getModerationButton()}
                          </div>
                        )}
                      </div>

                    </div>
                  )}
                </div>
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

          <CompactNav
            baseUrl={this.props.baseUrl}
            pages={this.props.pages}
            profile={this.props.profile}
          />

        </div>
      </div>
    );
    /* jshint ignore:end */
  }
}

/* jshint ignore:start */
export function IsDisabledMessage({ isActive, requestedDelete }) {
  if (isActive !== false && requestedDelete !== true) return null;

  let message = null;
  if (requestedDelete) {
    message = gettext("This user has requested for their account to be deleted.");
  } else {
    message = gettext("This user's account has been disabled by administrator.");
  }

  return (
    <div className="alert alert-danger">
      <p>{message}</p>
    </div>
  );
}

export function getColStyle(cols, col) {
  let colStyle = "";

  if (cols == 1) {
    colStyle = "col-xs-12";
  }

  if (cols == 2) {
    colStyle = "col-xs-6 col-sm-6";
  }

  if (cols == 3) {
    if (col == 2) {
      colStyle = "col-xs-12 col-sm-4 xs-margin-top";
    } else {
      colStyle += "col-xs-6 col-sm-4";
    }
  }

  return colStyle;
}
/* jshint ignore:end */