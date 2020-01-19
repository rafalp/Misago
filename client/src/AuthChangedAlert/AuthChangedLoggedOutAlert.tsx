import { Trans } from "@lingui/macro"
import React from "react"
import { Button, ButtonType } from "../UI"

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
        <p>
          <Trans id="auth_alert.logged_in.title">
            You have been logged out, <strong>{username}</strong>.
          </Trans>
        </p>
        <p>
          <Button
            text={
              <Trans id="auth_alert.logged_out.cta">
                This page was displayed while you were still logged in and is
                no longer accurate. Click this message to update page contents.
              </Trans>
            }
            type={ButtonType.LINK}
            onClick={reload}
          />
        </p>
      </div>
    </div>
  </div>
)

export default AuthChangedLoggedOutAlert
