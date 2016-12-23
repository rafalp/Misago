import React from 'react';
import { connect } from 'react-redux';
import Avatar from 'misago/components/avatar'; // jshint ignore:line
import ChangeAvatarModal, { select } from 'misago/components/change-avatar/root'; // jshint ignore:line
import misago from 'misago'; // jshint ignore:line
import dropdown from 'misago/services/mobile-navbar-dropdown';
import modal from 'misago/services/modal';

export class UserMenu extends React.Component {
  logout() {
    let decision = confirm(gettext("Are you sure you want to sign out?"));
    if (decision) {
      $('#hidden-logout-form').submit();
    }
  }

  changeAvatar() {
    modal.show(connect(select)(ChangeAvatarModal));
  }

  render() {
    /* jshint ignore:start */
    return (
      <ul
        className="dropdown-menu user-dropdown dropdown-menu-right"
        role="menu"
      >
        <li className="dropdown-header">
          <strong>{this.props.user.username}</strong>
        </li>
        <li className="divider" />
        <li>
          <a href={this.props.user.absolute_url}>
            <span className="material-icon">account_circle</span>
            {gettext("See your profile")}
          </a>
        </li>
        <li>
          <a href={misago.get('USERCP_URL')}>
            <span className="material-icon">done_all</span>
            {gettext("Change options")}
          </a>
        </li>
        <li>
          <button
            className="btn-link"
            onClick={this.changeAvatar}
            type="button"
          >
            <span className="material-icon">portrait</span>
            {gettext("Change avatar")}
          </button>
        </li>
        <li>
          <a href={misago.get('PRIVATE_THREADS_URL')}>
            <span className="material-icon">message</span>
            {gettext("Private threads")}
            <PrivateThreadsBadge user={this.props.user} />
          </a>
        </li>
        <li className="divider" />
        <li className="dropdown-buttons">
            <button
              className="btn btn-default btn-block"
              onClick={this.logout}
              type="button"
            >
              {gettext("Log out")}
            </button>
        </li>
      </ul>
    );
    /* jshint ignore:end */
  }
}

export function PrivateThreadsBadge(props) {
  if (!props.user.unread_private_threads) return null;

  /* jshint ignore:start */
  return (
    <span className="badge">
      {props.user.unread_private_threads}
    </span>
  );
  /* jshint ignore:end */

}

/* jshint ignore:start */
export function UserNav(props) {
    return (
      <ul className="ul nav navbar-nav nav-user">
        <UserPrivateThreadsLink user={props.user} />
        <li className="dropdown">
          <a
            aria-haspopup="true"
            aria-expanded="false"
            className="dropdown-toggle"
            data-toggle="dropdown"
            href={props.user.absolute_url}
            role="button"
          >
            <Avatar user={props.user} size="64" />
          </a>
          <UserMenu user={props.user} />
        </li>
      </ul>
    );
}
/* jshint ignore:end */

export function UserPrivateThreadsLink(props) {
  if (!props.user.unread_private_threads) return null;

  /* jshint ignore:start */
  return (
    <li>
      <a
        className="navbar-notification"
        href={misago.get('PRIVATE_THREADS_URL')}
        title={gettext("You have unread private threads.")}>
        <span className="material-icon">
          message
        </span>
        <span className="badge">
          {props.user.unread_private_threads}
        </span>
      </a>
    </li>
  );
  /* jshint ignore:end */
}

export function selectUserMenu(state) {
  return {user: state.auth.user};
}

export class CompactUserNav extends React.Component {
  showUserMenu() {
    dropdown.showConnected('user-menu', connect(selectUserMenu)(UserMenu));
  }

  render() {
    /* jshint ignore:start */
    return <button type="button" onClick={this.showUserMenu}>
      <Avatar user={this.props.user} size="64" />
    </button>;
    /* jshint ignore:end */
  }
}
