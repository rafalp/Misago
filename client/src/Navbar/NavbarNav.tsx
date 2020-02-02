import { Trans } from "@lingui/macro"
import React from "react"
import { AuthModalContext } from "../Context"
import { Button, ButtonType } from "../UI"
import { useAuth } from "../auth"
import { INavbarUserProp } from "./Navbar.types"
import UserDropdown from "./NavbarUserDropdown"

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
            <Button
              className="btn-logout"
              text={<Trans id="navbar.logout">Log out</Trans>}
              type={ButtonType.LINK}
              onClick={logout}
            />
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

export default NavbarNav
