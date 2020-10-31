import { Trans } from "@lingui/macro"
import React from "react"
import { ButtonLink } from "../UI/Button"

interface IAuthChangedLoggedOutAlertProps {
  username: string
  reload: () => void
}

const AuthChangedLoggedOutAlert: React.FC<IAuthChangedLoggedOutAlertProps> = ({
  username,
  reload,
}) => (
  <div className="auth-alert auth-alert-logged-out">
    <div className="alert alert-info">
      <div className="container-fluid">
        <p className="lead">
          <Trans id="auth_alert.logged_out.title">
            You have been logged out, <strong>{username}</strong>.
          </Trans>
        </p>
        <p>
          <ButtonLink
            text={
              <Trans id="auth_alert.logged_out.cta">
                This page was displayed while you were still logged in and is
                no longer accurate. Click this message to update its contents.
              </Trans>
            }
            onClick={reload}
          />
        </p>
      </div>
    </div>
  </div>
)

export default AuthChangedLoggedOutAlert
