import { Trans } from "@lingui/macro"
import React from "react"
import { AuthModalContext } from "../Context"
import { ButtonLink } from "../UI"
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
            <ButtonLink
              className="btn-logout"
              text={<Trans id="navbar.logout">Log out</Trans>}
              onClick={logout}
            />
          </li>
        </>
      ) : (
        <>
          <li className="nav-item d-sm-block">
            <ButtonLink
              className="btn-login"
              text={<Trans id="navbar.login">Log in</Trans>}
              onClick={openLoginModal}
            />
          </li>
          <li className="nav-item d-sm-block">
            <ButtonLink
              className="btn-register"
              text={<Trans id="navbar.register">Sign up</Trans>}
              onClick={openRegisterModal}
            />
          </li>
        </>
      )}
    </ul>
  )
}

export default NavbarNav
