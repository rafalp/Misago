import React from 'react';
import { connect } from 'react-redux';
import Avatar from 'misago/components/avatar'; // jshint ignore:line
import misago from 'misago/index'; // jshint ignore:line
import dropdown from 'misago/services/mobile-navbar-dropdown';

export class UserMenu extends React.Component {
  logout() {
    let decision = confirm(gettext("Are you sure you want to sign out?"));
    if (decision) {
      $('#hidden-logout-form').submit();
    }
  }

  render() {
    /* jshint ignore:start */
    return <ul className="dropdown-menu user-dropdown dropdown-menu-right"
               role="menu">
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
        <button type="button" className="btn-link">
          <span className="material-icon">face</span>
          {gettext("Change avatar")}
        </button>
      </li>
      <li className="divider" />
      <li className="dropdown-footer">
          <button type="button" className="btn btn-default btn-block"
                  onClick={this.logout}>
            {gettext("Log out")}
          </button>
      </li>
    </ul>;
    /* jshint ignore:end */
  }
}

export class UserNav extends React.Component {
  render() {
    /* jshint ignore:start */
    return <ul className="ul nav navbar-nav nav-user">
      <li className="dropdown">
        <a href={this.props.user.absolute_url} className="dropdown-toggle"
           data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"
           role="button">
          <Avatar user={this.props.user} size="64" />
        </a>
        <UserMenu user={this.props.user} />
      </li>
    </ul>;
    /* jshint ignore:end */
  }
}

export function selectUserMenu(store) {
  return {user: store.auth.user};
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
