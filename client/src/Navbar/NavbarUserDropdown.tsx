import { Trans } from "@lingui/macro"
import React from "react"
import { Avatar, Button, ButtonType, Dropdown, DropdownButton } from "../UI"

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
          type={ButtonType.LINK}
          onClick={toggle}
        />
      </li>
    )}
    menu={
      <>
        <h6 className="dropdown-header">{user.name}</h6>
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
