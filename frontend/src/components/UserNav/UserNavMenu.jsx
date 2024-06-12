import classnames from "classnames"
import React from "react"
import { connect } from "react-redux"
import modal from "../../services/modal"
import ChangeAvatarModal, {
  select as selectAvatar,
} from "../change-avatar/root"
import {
  DropdownDivider,
  DropdownFooter,
  DropdownMenuItem,
  DropdownSubheader,
} from "../Dropdown"
import logout from "./logout"

class UserNavMenu extends React.Component {
  constructor(props) {
    super(props)

    if (props.dropdown) {
      // Collapse options on dropdown
      this.state = {
        options: props.options.slice(0, 2),
        optionsMore: props.options.length > 2,
      }
    } else {
      // Reveal all options on mobile overlay
      this.state = {
        options: props.options,
        optionsMore: false,
      }
    }
  }

  changeAvatar = () => {
    this.props.close()
    modal.show(connect(selectAvatar)(ChangeAvatarModal))
  }

  revealOptions = () => {
    this.setState({
      options: this.props.options,
      optionsMore: false,
    })
  }

  render() {
    const { user, close, dropdown, overlay } = this.props

    if (!user) {
      return null
    }

    const adminUrl = misago.get("ADMIN_URL")

    return (
      <ul
        className={classnames("user-nav-menu", {
          "dropdown-menu-list": dropdown,
          "overlay-menu-list": overlay,
        })}
      >
        <li className="dropdown-menu-item">
          <a href={user.url} className="user-nav-profile">
            <strong>{user.username}</strong>
            <small>{pgettext("user nav", "Go to your profile")}</small>
          </a>
        </li>
        <DropdownDivider />
        <DropdownMenuItem>
          <a href={misago.get("NOTIFICATIONS_URL")}>
            <span className="material-icon">
              {user.unreadNotifications
                ? "notifications_active"
                : "notifications_none"}
            </span>
            {pgettext("user nav", "Notifications")}
            {!!user.unreadNotifications && (
              <span className="badge">{user.unreadNotifications}</span>
            )}
          </a>
        </DropdownMenuItem>
        {!!user.showPrivateThreads && (
          <DropdownMenuItem>
            <a href={misago.get("PRIVATE_THREADS_URL")}>
              <span className="material-icon">inbox</span>
              {pgettext("user nav", "Private threads")}
              {!!user.unreadPrivateThreads && (
                <span className="badge">{user.unreadPrivateThreads}</span>
              )}
            </a>
          </DropdownMenuItem>
        )}
        {!!adminUrl && (
          <DropdownMenuItem>
            <a href={adminUrl} target="_blank">
              <span className="material-icon">security</span>
              {pgettext("user nav", "Admin control panel")}
            </a>
          </DropdownMenuItem>
        )}
        <DropdownDivider />
        <DropdownSubheader className="user-nav-options">
          {pgettext("user nav section", "Account settings")}
        </DropdownSubheader>
        <DropdownMenuItem>
          <button
            className="btn-link"
            onClick={this.changeAvatar}
            type="button"
          >
            <span className="material-icon">portrait</span>
            {pgettext("user nav", "Change avatar")}
          </button>
        </DropdownMenuItem>
        {this.state.options.map((item) => (
          <DropdownMenuItem key={item.icon}>
            <a href={item.url}>
              <span className="material-icon">{item.icon}</span>
              {item.name}
            </a>
          </DropdownMenuItem>
        ))}
        <DropdownMenuItem>
          <button
            className={classnames("btn-link", {
              "d-none": !this.state.optionsMore,
            })}
            onClick={this.revealOptions}
            type="button"
          >
            <span className="material-icon">more_vertical</span>
            {pgettext("user nav", "See more")}
          </button>
        </DropdownMenuItem>
        {!!dropdown && (
          <DropdownFooter listItem>
            <button
              className="btn btn-default btn-block"
              onClick={() => {
                logout()
                close()
              }}
              type="button"
            >
              {pgettext("user nav", "Log out")}
            </button>
          </DropdownFooter>
        )}
      </ul>
    )
  }
}

function select(state) {
  const user = state.auth.user
  if (!user.id) {
    return { user: null }
  }

  return {
    user: {
      username: user.username,
      unreadNotifications: user.unreadNotifications,
      unreadPrivateThreads: user.unread_private_threads,
      showPrivateThreads: user.acl.can_use_private_threads,
      url: user.url,
    },
    options: [...misago.get("userOptions")],
  }
}

const UserNavMenuConnected = connect(select)(UserNavMenu)

export default UserNavMenuConnected
