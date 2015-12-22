import React from 'react';
import GuestNav from 'misago/components/user-menu/guest-nav'; // jshint ignore:line
import UserNav from 'misago/components/user-menu/user-nav'; // jshint ignore:line

export class UserMenu extends React.Component {
  render() {
    /* jshint ignore:start */
    if (this.props.isAuthenticated) {
      return <UserNav user={this.props.user} />;
    } else {
      return <GuestNav />;
    }
    /* jshint ignore:end */
  }
}

export function select(state) {
  return state.auth;
}
