import React from 'react';
import Button from 'misago/components/button'; // jshint ignore:line

import modal from 'misago/services/modal';
import dropdown from 'misago/services/mobile-navbar-dropdown';
import Avatar from 'misago/components/avatar'; // jshint ignore:line
import SignInModal from 'misago/components/sign-in.js';
import RegisterModal from 'misago/components/register/root.js';

export class GuestMenu extends React.Component {
  showSignInModal() {
    modal.show(SignInModal);
  }

  showRegisterModal() {
    modal.show(RegisterModal);
  }

  render() {
    /* jshint ignore:start */
    return <ul className="dropdown-menu user-dropdown dropdown-menu-right"
               role="menu">
      <li className="guest-preview">
        <h4>{gettext("You are browsing as guest.")}</h4>
        <p>
          {gettext('Sign in or register to start and participate in discussions.')}
        </p>
        <div className="row">

          <div className="col-xs-6">
            <button type="button" className="btn btn-default btn-block">
              Thy Sign In
            </button>

          </div>
          <div className="col-xs-6">

            <button type="button" className="btn btn-primary btn-block">
              Thy Registry
            </button>

          </div>
        </div>
      </li>
    </ul>;
    /* jshint ignore:end */
  }
}

export class GuestNav extends GuestMenu {
  render() {
    /* jshint ignore:start */
    return <div className="nav nav-guest">
      <Button type="button"
              className="navbar-btn btn-default"
              onClick={this.showSignInModal}>
        Sign in
      </Button>
      <Button type="button"
              className="navbar-btn btn-primary"
              onClick={this.showRegisterModal}>
        Register
      </Button>
    </div>;
    /* jshint ignore:end */
  }
}

export class CompactGuestNav extends React.Component {
  showGuestMenu() {
    dropdown.show(GuestMenu);
  }

  render() {
    /* jshint ignore:start */
    return <button type="button" onClick={this.showGuestMenu}>
      <Avatar size="64" />
    </button>;
    /* jshint ignore:end */
  }
}
