import { Trans } from "@lingui/macro"
import React from "react"
import { ButtonLink } from "../UI/Button"

interface AuthChangedLoggedInAlertProps {
  username: string
  reload: () => void
}

const AuthChangedLoggedInAlert: React.FC<AuthChangedLoggedInAlertProps> = ({
  username,
  reload,
}) => (
  <div className="auth-alert auth-alert-logged-in">
    <div className="alert alert-info">
      <div className="container-fluid">
        <p className="lead">
          <Trans id="auth_alert.logged_in.title">
            You have been logged in, <strong>{username}</strong>.
          </Trans>
        </p>
        <p>
          <ButtonLink
            text={
              <Trans id="auth_alert.logged_in.cta">
                This page was displayed before you've logged in and is no
                longer accurate. Click this message to update its contents.
              </Trans>
            }
            onClick={reload}
          />
        </p>
      </div>
    </div>
  </div>
)

export default AuthChangedLoggedInAlert
