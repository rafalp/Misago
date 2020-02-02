import { Trans } from "@lingui/macro"
import React from "react"
import { AuthModalContext } from "../Context"
import { Avatar, Button, ButtonType, Dropdown } from "../UI"
import { useAuth } from "../auth"
import { INavbarUserProp } from "./Navbar.types"

interface INavbarNavProps {
  user?: INavbarUserProp | null
}

const NavbarNav: React.FC<INavbarNavProps> = ({ user }) => {
  const { logout } = useAuth()
  const { openLoginModal, openRegisterModal } = React.useContext(
    AuthModalContext
  )

  return (
    <ul className="navbar-nav ml-auto">
      {user ? (
        <>
          <UserDropdown logout={logout} user={user} />
          <li className="nav-item d-sm-none">
            <button
              className="btn btn-block border-0 nav-link text-left"
              type="button"
              onClick={logout}
            >
              <Trans id="navbar.logout">Log out</Trans>
            </button>
          </li>
        </>
      ) : (
        <>
          <li className="nav-item d-sm-block">
            <Button
              className="btn-login"
              text={<Trans id="navbar.login">Log in</Trans>}
              type={ButtonType.LINK}
              onClick={openLoginModal}
            />
          </li>
          <li className="nav-item d-sm-block">
            <Button
              className="btn-register"
              text={<Trans id="navbar.register">Sign up</Trans>}
              type={ButtonType.LINK}
              onClick={openRegisterModal}
            />
          </li>
        </>
      )}
    </ul>
  )
}

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
          type={ButtonType.LINK}
          onClick={toggle}
          text={user.name}
        />
      </li>
    )}
    menu={
      <>
        <h6 className="dropdown-header">{user.name}</h6>
        <button className="dropdown-item" type="button" onClick={logout}>
          <Trans id="navbar.logout">Log out</Trans>
        </button>
      </>
    }
  />
)

export default NavbarNav
