import { t } from "@lingui/macro"
import { I18n } from "@lingui/react"
import React from "react"
import { Link } from "react-router-dom"
import { AuthModalContext } from "../Context"
import { Button } from "../UI"
import { useAuth } from "../auth"
import { INavbarProps } from "./Navbar.types"

const Navbar: React.FC<INavbarProps> = ({ settings, user }) => {
  const { logout } = useAuth()
  const { openLoginModal, openRegisterModal } = React.useContext(
    AuthModalContext
  )

  if (!settings) return null

  return (
    <I18n>
      {({ i18n }) => (
        <nav className="navbar navbar-light bg-white">
          <div className="container-fluid">
            <Link className="navbar-brand" to="/">
              {settings.forumName}
            </Link>
            {user ? (
              <div className="row">
                <div className="col-auto">
                  <img
                    src={user.avatars[0].url}
                    width="32"
                    height="32"
                    alt=""
                  />
                  {`Hello, ${user.name}`}
                </div>
                <div className="col-auto">
                  <Button
                    text={i18n._(t("navbar.logout")`Log out`)}
                    onClick={logout}
                  />
                </div>
              </div>
            ) : (
              <div className="row">
                <div className="col-auto">
                  <Button
                    text={i18n._(t("navbar.login")`Log in`)}
                    onClick={openLoginModal}
                  />
                </div>
                <div className="col-auto">
                  <Button
                    text={i18n._(t("navbar.register")`Sign up`)}
                    onClick={openRegisterModal}
                  />
                </div>
              </div>
            )}
          </div>
        </nav>
      )}
    </I18n>
  )
}

export default Navbar
