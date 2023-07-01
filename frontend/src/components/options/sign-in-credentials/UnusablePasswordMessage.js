import React from "react"
import misago from "misago/index"

const UnusablePasswordMessage = () => {
  return (
    <div className="panel panel-default panel-form">
      <div className="panel-heading">
        <h3 className="panel-title">
          {pgettext(
            "change sign in credentials title",
            "Change email or password"
          )}
        </h3>
      </div>
      <div className="panel-body panel-message-body">
        <div className="message-icon">
          <span className="material-icon">info_outline</span>
        </div>
        <div className="message-body">
          <p className="lead">
            {pgettext(
              "change sign in credentials",
              "You need to set a password for your account to be able to change your username or email."
            )}
          </p>
          <p className="help-block">
            <a
              className="btn btn-primary"
              href={misago.get("FORGOTTEN_PASSWORD_URL")}
            >
              {pgettext("change sign in credentials link", "Set password")}
            </a>
          </p>
        </div>
      </div>
    </div>
  )
}

export default UnusablePasswordMessage
