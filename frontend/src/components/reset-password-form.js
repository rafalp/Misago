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

      password: ""
    }
  }

  clean() {
    if (this.state.password.trim().length) {
      return true
    } else {
      snackbar.error(gettext("Enter new password."))
      return false
    }
  }

  send() {
    return ajax.post(misago.get("CHANGE_PASSWORD_API"), {
      password: this.state.password
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
                placeholder={gettext("Enter new password")}
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
            {gettext("Change password")}
          </Button>
        </form>
      </div>
    )
  }
}

export class PasswordChangedPage extends React.Component {
  getMessage() {
    return interpolate(
      gettext("%(username)s, your password has been changed successfully."),
      {
        username: this.props.user.username
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
                {gettext(
                  "You will have to sign in using new password before continuing."
                )}
              </p>
              <p>
                <button
                  type="button"
                  className="btn btn-primary"
                  onClick={this.showSignIn}
                >
                  {gettext("Sign in")}
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
  complete = apiResponse => {
    auth.softSignOut()

    // nuke "redirect_to" field so we don't end
    // coming back to error page after sign in
    $('#hidden-login-form input[name="redirect_to"]').remove()

    ReactDOM.render(
      <PasswordChangedPage user={apiResponse} />,
      document.getElementById("page-mount")
    )
  }

  render() {
    return <ResetPasswordForm callback={this.complete} />
  }
}
