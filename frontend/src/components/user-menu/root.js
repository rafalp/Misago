import React from 'react';
import { GuestNav, CompactGuestNav } from './guest-nav'; // jshint ignore:line
import { UserNav, CompactUserNav} from './user-nav'; // jshint ignore:line

export class UserMenu extends React.Component {
  render() {
    /* jshint ignore:start */
    if (this.props.isAuthenticated) {
      return (
        <UserNav user={this.props.user} />
      );
    } else {
      return (
        <GuestNav />
      );
    }
    /* jshint ignore:end */
  }
}

export class CompactUserMenu extends React.Component {
  render() {
    /* jshint ignore:start */
    if (this.props.isAuthenticated) {
      return (
        <CompactUserNav user={this.props.user} />
      );
    } else {
      return (
        <CompactGuestNav />
      );
    }
    /* jshint ignore:end */
  }
}

export function select(state) {
  return state.auth;
}
