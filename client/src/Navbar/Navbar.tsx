import { t } from "@lingui/macro"
import { I18n } from "@lingui/react"
import React from "react"
import { Link } from "react-router-dom"
import { Button } from "../UI"
import { INavbarProps } from "./Navbar.types"

const Navbar: React.FC<INavbarProps> = ({ openRegister, settings, user }) => {
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
              <div>
                <img src={user.avatars[0].url} width="40" height="40" alt="" />
                {`Hello, ${user.name}`}
              </div>
            ) : (
              <div className="row">
                <div className="col">
                  <Button text={i18n._(t("btn.login")`Log in`)} />
                </div>
                <div className="col">
                  <Button text={i18n._(t("btn.register")`Register`)} onClick={openRegister} />
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
