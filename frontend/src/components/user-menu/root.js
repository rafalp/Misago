import React from "react"
import { GuestNav, CompactGuestNav } from "./guest-nav"
import { UserNav, CompactUserNav } from "./user-nav"

export class UserMenu extends React.Component {
  render() {
    if (this.props.isAuthenticated) {
      return <UserNav user={this.props.user} />
    } else {
      return <GuestNav />
    }
  }
}

export class CompactUserMenu extends React.Component {
  render() {
    if (this.props.isAuthenticated) {
      return <CompactUserNav user={this.props.user} />
    } else {
      return <CompactGuestNav />
    }
  }
}

export function select(state) {
  return state.auth
}
