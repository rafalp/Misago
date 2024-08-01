import React from "react"
import ReactDOM from "react-dom"
import misago from "misago/index"
import Button from "misago/components/button"
import Form from "misago/components/form"
import SignInModal from "misago/components/sign-in.js"
import ajax from "misago/services/ajax"
import auth from "misago/services/auth"
import modal from "misago/services/modal"
import snackbar from "misago/services/snackbar"
import showBannedPage from "misago/utils/banned-page"

export class ResetPasswordForm extends Form {
  constructor(props) {
    super(props)

    this.state = {
      isLoading: false,

      password: "",
    }
  }

  clean() {
    if (this.state.password.trim().length) {
      return true
    } else {
      snackbar.error(pgettext("password reset form", "Enter new password."))
      return false
    }
  }

  send() {
    return ajax.post(misago.get("CHANGE_PASSWORD_API"), {
      password: this.state.password,
    })
  }

  handleSuccess(apiResponse) {
    this.props.callback(apiResponse)
  }

  handleError(rejection) {
    if (rejection.status === 403 && rejection.ban) {
      showBannedPage(rejection.ban)
    } else {
      snackbar.apiError(rejection)
    }
  }

  render() {
    return (
      <div className="well well-form well-form-reset-password">
        <form onSubmit={this.handleSubmit}>
          <div className="form-group">
            <div className="control-input">
              <input
                type="password"
                className="form-control"
                placeholder={pgettext(
                  "password reset form field",
                  "Enter new password"
                )}
                disabled={this.state.isLoading}
                onChange={this.bindInput("password")}
                value={this.state.password}
              />
            </div>
          </div>

          <Button
            className="btn-primary btn-block"
            loading={this.state.isLoading}
          >
            {pgettext("password reset form btn", "Change password")}
          </Button>
        </form>
      </div>
    )
  }
}

export class PasswordChangedPage extends React.Component {
  getMessage() {
    return interpolate(
      pgettext(
        "password reset form",
        "%(username)s, your password has been changed."
      ),
      {
        username: this.props.user.username,
      },
      true
    )
  }

  showSignIn() {
    modal.show(SignInModal)
  }

  render() {
    return (
      <div className="page page-message page-message-success page-forgotten-password-changed">
        <div className="container">
          <div className="message-panel">
            <div className="message-icon">
              <span className="material-icon">check</span>
            </div>

            <div className="message-body">
              <p className="lead">{this.getMessage()}</p>
              <p>
                {pgettext(
                  "password reset form",
                  "Sign in using new password to continue."
                )}
              </p>
              <p>
                <button
                  type="button"
                  className="btn btn-primary"
                  onClick={this.showSignIn}
                >
                  {pgettext("password reset form btn", "Sign in")}
                </button>
              </p>
            </div>
          </div>
        </div>
      </div>
    )
  }
}

export default class extends React.Component {
  complete = (apiResponse) => {
    auth.softSignOut()

    // nuke "next" field so we don't end
    // coming back to error page after sign in
    $('#hidden-login-form input[name="next"]').remove()

    ReactDOM.render(
      <PasswordChangedPage user={apiResponse} />,
      document.getElementById("page-mount")
    )
  }

  render() {
    return <ResetPasswordForm callback={this.complete} />
  }
}
