import { Trans } from "@lingui/macro"
import React from "react"
import { Link } from "react-router-dom"
import { useAuthModalContext, useSettingsContext } from "../Context"
import { Button } from "../UI"
import { useAuth } from "../auth"
import * as urls from "../urls"
import { INavbarUserProp } from "./Navbar.types"
import UserDropdown from "./NavbarUserDropdown"

interface INavbarNavProps {
  user?: INavbarUserProp | null
}

const NavbarNav: React.FC<INavbarNavProps> = ({ user }) => {
  const { logout } = useAuth()
  const settings = useSettingsContext()
  const { openLoginModal, openRegisterModal } = useAuthModalContext()

  return (
    <ul className="navbar-nav ml-auto">
      <li className="nav-item">
        <Link className="nav-link" to="/">
          {settings?.forumIndexThreads ? (
            <Trans id="navbar.threads">Threads</Trans>
          ) : (
            <Trans id="navbar.categories">Categories</Trans>
          )}
        </Link>
      </li>
      <li className="nav-item">
        {settings?.forumIndexThreads ? (
          <Link className="nav-link" to={urls.categories()}>
            <Trans id="navbar.categories">Categories</Trans>
          </Link>
        ) : (
          <Link className="nav-link" to={urls.threads()}>
            <Trans id="navbar.threads">Threads</Trans>
          </Link>
        )}
      </li>
      {user ? (
        <>
          <UserDropdown logout={logout} user={user} />
          <li className="nav-item d-sm-none">
            <Button
              className="btn-logout"
              text={<Trans id="navbar.logout">Log out</Trans>}
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
              onClick={openLoginModal}
            />
          </li>
          <li className="nav-item d-sm-block">
            <Button
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
