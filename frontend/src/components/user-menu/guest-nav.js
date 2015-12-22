import React from 'react';
import Button from 'misago/components/button'; // jshint ignore:line

import modal from 'misago/services/modal';
import SignInModal from 'misago/components/sign-in/root.js';
import RegisterModal from 'misago/components/register/root.js';

export default class GuestNav extends React.Component {
  showSignInModal() {
    modal.show(SignInModal);
  }

  showRegisterModal() {
    modal.show(RegisterModal);
  }

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
