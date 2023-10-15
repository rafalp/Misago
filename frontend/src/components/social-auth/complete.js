import React from "react"
import misago from "misago"
import PageContainer from "../PageContainer"
import Header from "./header"

const Complete = ({ activation, backend_name, username }) => {
  let icon = ""
  let message = ""
  if (activation === "user") {
    message = pgettext(
      "account activation required",
      "%(username)s, your account has been created but you need to activate it before you will be able to sign in."
    )
  } else if (activation === "admin") {
    message = pgettext(
      "account activation required",
      "%(username)s, your account has been created but the site administrator will have to activate it before you will be able to sign in."
    )
  } else {
    message = pgettext(
      "social auth complete",
      "%(username)s, your account has been created and you have been signed in to it."
    )
  }

  if (activation === "active") {
    icon = "check"
  } else {
    icon = "info_outline"
  }

  return (
    <div className="page page-social-auth page-social-auth-register">
      <Header backendName={backend_name} />
      <PageContainer>
        <div className="row">
          <div className="col-md-6 col-md-offset-3">
            <div className="panel panel-default panel-form">
              <div className="panel-heading">
                <h3 className="panel-title">
                  {pgettext(
                    "social auth complete title",
                    "Registration completed!"
                  )}
                </h3>
              </div>
              <div className="panel-body panel-message-body">
                <div className="message-icon">
                  <span className="material-icon">{icon}</span>
                </div>
                <div className="message-body">
                  <p className="lead">
                    {interpolate(message, { username }, true)}
                  </p>
                  <p className="help-block">
                    <a
                      className="btn btn-default"
                      href={misago.get("MISAGO_PATH")}
                    >
                      {pgettext(
                        "social auth complete link",
                        "Return to forum index"
                      )}
                    </a>
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </PageContainer>
    </div>
  )
}

export default Complete
