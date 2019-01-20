import React from "react"
import { connect } from "react-redux"
import Avatar from "misago/components/avatar"
import ChangeAvatarModal, { select } from "misago/components/change-avatar/root"
import NavbarSearch from "misago/components/navbar-search"
import misago from "misago"
import dropdown from "misago/services/mobile-navbar-dropdown"
import modal from "misago/services/modal"

export class UserMenu extends React.Component {
  logout() {
    let decision = confirm(gettext("Are you sure you want to sign out?"))
    if (decision) {
      $("#hidden-logout-form").submit()
    }
  }

  changeAvatar() {
    modal.show(connect(select)(ChangeAvatarModal))
  }

  render() {
    const { user } = this.props

    return (
      <ul
        className="dropdown-menu user-dropdown dropdown-menu-right"
        role="menu"
      >
        <li className="dropdown-header">
          <strong>{user.username}</strong>
          <div className="row user-stats">
            <div className="col-sm-3">
              <span className="material-icon">message</span>
              {user.posts}
            </div>
            <div className="col-sm-3">
              <span className="material-icon">forum</span>
              {user.threads}
            </div>
            <div className="col-sm-3">
              <span className="material-icon">favorite</span>
              {user.followers}
            </div>
            <div className="col-sm-3">
              <span className="material-icon">favorite_outline</span>
              {user.following}
            </div>
          </div>
        </li>
        <li className="divider" />
        <li>
          <a href={user.url}>
            <span className="material-icon">account_circle</span>
            {gettext("See your profile")}
          </a>
        </li>
        <li>
          <a href={misago.get("USERCP_URL")}>
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
        {!!user.acl.can_use_private_threads && (
          <li>
            <a href={misago.get("PRIVATE_THREADS_URL")}>
              <span className="material-icon">message</span>
              {gettext("Private threads")}
              <PrivateThreadsBadge user={user} />
            </a>
          </li>
        )}
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
    )
  }
}

export function PrivateThreadsBadge({ user }) {
  if (!user.unread_private_threads) return null

  return <span className="badge">{user.unread_private_threads}</span>
}

export function UserNav({ user }) {
  return (
    <ul className="ul nav navbar-nav nav-user">
      <li>
        <NavbarSearch />
      </li>
      <UserPrivateThreadsLink user={user} />
      <li className="dropdown">
        <a
          aria-haspopup="true"
          aria-expanded="false"
          className="dropdown-toggle"
          data-toggle="dropdown"
          href={user.url}
          role="button"
        >
          <Avatar user={user} size="64" />
        </a>
        <UserMenu user={user} />
      </li>
    </ul>
  )
}

export function UserPrivateThreadsLink({ user }) {
  if (!user.acl.can_use_private_threads) return null

  let title = null
  if (user.unread_private_threads) {
    title = gettext("You have unread private threads!")
  } else {
    title = gettext("Private threads")
  }

  return (
    <li>
      <a
        className="navbar-icon"
        href={misago.get("PRIVATE_THREADS_URL")}
        title={title}
      >
        <span className="material-icon">message</span>
        {user.unread_private_threads > 0 && (
          <span className="badge">{user.unread_private_threads}</span>
        )}
      </a>
    </li>
  )
}

export function selectUserMenu(state) {
  return {
    user: state.auth.user
  }
}

export class CompactUserNav extends React.Component {
  showUserMenu() {
    dropdown.showConnected("user-menu", connect(selectUserMenu)(UserMenu))
  }

  render() {
    return (
      <button type="button" onClick={this.showUserMenu}>
        <Avatar user={this.props.user} size="50" />
      </button>
    )
  }
}
