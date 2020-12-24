import { Trans } from "@lingui/macro"
import React from "react"
import Avatar from "../UI/Avatar"
import { Button } from "../UI/Button"
import { Dropdown, DropdownButton, DropdownLink } from "../UI/Dropdown"
import * as urls from "../urls"

import { User } from "./Navbar.types"

interface NavbarUserDropdownProps {
  logout: () => void
  user: User
}

const NavbarUserDropdown: React.FC<NavbarUserDropdownProps> = ({ logout, user }) => (
  <Dropdown
    className="dropdown-menu-user"
    toggle={({ ref, toggle }) => (
      <li className={"nav-item dropdown d-xs-none d-sm-block"}>
        <Button
          elementRef={ref}
          image={<Avatar alt={user.name} size={32} user={user} />}
          onClick={toggle}
        />
      </li>
    )}
    menu={() => (
      <>
        <h6 className="dropdown-header">{user.name}</h6>
        <DropdownLink
          text={<Trans id="navbar.profile">See your profile</Trans>}
          to={urls.user(user)}
        />
        <DropdownButton
          className="dropdown-item-logout"
          text={<Trans id="navbar.logout">Log out</Trans>}
          onClick={logout}
        />
      </>
    )}
  />
)

export default NavbarUserDropdown
