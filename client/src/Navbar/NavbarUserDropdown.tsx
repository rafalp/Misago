import { Trans } from "@lingui/macro"
import React from "react"
import { Avatar, Button, Dropdown, DropdownButton, DropdownLink } from "../UI"
import * as urls from "../urls"

import { INavbarUserProp } from "./Navbar.types"

interface IUserDropdownProps {
  logout: () => void
  user: INavbarUserProp
}

const UserDropdown: React.FC<IUserDropdownProps> = ({ logout, user }) => (
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
    menu={
      <>
        <h6 className="dropdown-header">{user.name}</h6>
        <DropdownLink to={urls.user(user)}>
          <Trans id="navbar.profile">See your profile</Trans>
        </DropdownLink>
        <DropdownButton
          className="dropdown-item-logout"
          text={<Trans id="navbar.logout">Log out</Trans>}
          onClick={logout}
        />
      </>
    }
  />
)

export default UserDropdown
