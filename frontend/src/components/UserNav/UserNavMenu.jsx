import classnames from "classnames"
import React from "react"
import { connect } from "react-redux"
import {
  DropdownDivider,
  DropdownFooter,
  DropdownMenuItem,
  DropdownSubheader,
} from "../Dropdown"
import logout from "./logout"

function UserNavMenu({ user, close, dropdown, overlay }) {
  if (!user) {
    return null
  }

  return (
    <ul
      className={classnames("user-nav-menu", {
        "dropdown-menu-list": dropdown,
        "overlay-menu-list": overlay,
      })}
    >
      <li className="dropdown-header user-nav-header">{user.username}</li>
      {!!dropdown && (
        <DropdownFooter>
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

function select(state) {
  const user = state.auth.user
  if (!user.id) {
    return { user: null }
  }

  return {
    user: {
      username: user.username,
      url: user.url,
    },
  }
}

const UserNavMenuConnected = connect(select)(UserNavMenu)

export default UserNavMenuConnected
