import React from 'react';
import Avatar from 'misago/components/avatar'; // jshint ignore:line
import RegisterButton from 'misago/components/register-button'; // jshint ignore:line
import SignInModal from 'misago/components/sign-in.js';
import dropdown from 'misago/services/mobile-navbar-dropdown';
import modal from 'misago/services/modal';

export class GuestMenu extends React.Component {
  showSignInModal() {
    modal.show(SignInModal);
  }

  render() {
    /* jshint ignore:start */
    return (
      <ul
        className="dropdown-menu user-dropdown dropdown-menu-right"
        role="menu"
      >
        <li className="guest-preview">
          <h4>{gettext("You are browsing as guest.")}</h4>
          <p>
            {gettext('Sign in or register to start and participate in discussions.')}
          </p>
          <div className="row">
            <div className="col-xs-6">

              <button
                className="btn btn-default btn-block"
                onClick={this.showSignInModal}
                type="button"
              >
                {gettext("Sign in")}
              </button>

            </div>
            <div className="col-xs-6">

              <RegisterButton className="btn-success btn-block">
                {gettext("Register")}
              </RegisterButton>

            </div>
          </div>
        </li>
      </ul>
    );
    /* jshint ignore:end */
  }
}

export class GuestNav extends GuestMenu {
  render() {
    /* jshint ignore:start */
    return (
      <div className="nav nav-guest">
        <button
          className="btn navbar-btn btn-default"
          onClick={this.showSignInModal}
          type="button"
        >
          {gettext("Sign in")}
        </button>
        <RegisterButton className="navbar-btn btn-success btn-outline">
          {gettext("Register")}
        </RegisterButton>
      </div>
    );
    /* jshint ignore:end */
  }
}

export class CompactGuestNav extends React.Component {
  showGuestMenu() {
    dropdown.show(GuestMenu);
  }

  render() {
    /* jshint ignore:start */
    return (
      <button type="button" onClick={this.showGuestMenu}>
        <Avatar size="64" />
      </button>
    );
    /* jshint ignore:end */
  }
}
