import React from "react"
import ReactDOM from "react-dom"
import misago from "misago/index"
import Button from "misago/components/button"
import Form from "misago/components/form"
import ajax from "misago/services/ajax"
import snackbar from "misago/services/snackbar"
import * as validators from "misago/utils/validators"
import showBannedPage from "misago/utils/banned-page"

export class RequestResetForm extends Form {
  constructor(props) {
    super(props)

    this.state = {
      isLoading: false,

      email: "",

      validators: {
        email: [validators.email()],
      },
    }
  }

  clean() {
    if (this.isValid()) {
      return true
    } else {
      snackbar.error(
        pgettext("request password reset form", "Enter a valid e-mail address.")
      )
      return false
    }
  }

  send() {
    return ajax.post(misago.get("SEND_PASSWORD_RESET_API"), {
      email: this.state.email,
    })
  }

  handleSuccess(apiResponse) {
    this.props.callback(apiResponse)
  }

  handleError(rejection) {
    if (["inactive_user", "inactive_admin"].indexOf(rejection.code) > -1) {
      this.props.showInactivePage(rejection)
    } else if (rejection.status === 403 && rejection.ban) {
      showBannedPage(rejection.ban)
    } else {
      snackbar.apiError(rejection)
    }
  }

  render() {
    return (
      <div className="well well-form well-form-request-password-reset">
        <form onSubmit={this.handleSubmit}>
          <div className="form-group">
            <div className="control-input">
              <input
                type="text"
                className="form-control"
                placeholder={pgettext(
                  "request password reset form field",
                  "Your e-mail address"
                )}
                disabled={this.state.isLoading}
                onChange={this.bindInput("email")}
                value={this.state.email}
              />
            </div>
          </div>

          <Button
            className="btn-primary btn-block"
            loading={this.state.isLoading}
          >
            {pgettext("request password reset form btn", "Send link")}
          </Button>
        </form>
      </div>
    )
  }
}

export class LinkSent extends React.Component {
  getMessage() {
    return interpolate(
      pgettext(
        "request password reset form",
        "Reset password link was sent to %(email)s"
      ),
      {
        email: this.props.user.email,
      },
      true
    )
  }

  render() {
    return (
      <div className="well well-form well-form-request-password-reset well-done">
        <div className="done-message">
          <div className="message-icon">
            <span className="material-icon">check</span>
          </div>
          <div className="message-body">
            <p>{this.getMessage()}</p>
          </div>
          <button
            type="button"
            className="btn btn-primary btn-block"
            onClick={this.props.callback}
          >
            {pgettext(
              "request password reset form btn",
              "Request another link"
            )}
          </button>
        </div>
      </div>
    )
  }
}

export class AccountInactivePage extends React.Component {
  getActivateButton() {
    if (this.props.activation === "inactive_user") {
      return (
        <p>
          <a href={misago.get("REQUEST_ACTIVATION_URL")}>
            {pgettext(
              "request password reset form error",
              "Activate your account."
            )}
          </a>
        </p>
      )
    } else {
      return null
    }
  }

  render() {
    return (
      <div className="page page-message page-message-info page-forgotten-password-inactive">
        <div className="container">
          <div className="message-panel">
            <div className="message-icon">
              <span className="material-icon">info_outline</span>
            </div>

            <div className="message-body">
              <p className="lead">
                {pgettext(
                  "request password reset form error",
                  "Your account is inactive."
                )}
              </p>
              <p>{this.props.message}</p>
              {this.getActivateButton()}
            </div>
          </div>
        </div>
      </div>
    )
  }
}

export default class extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      complete: false,
    }
  }

  complete = (apiResponse) => {
    this.setState({
      complete: apiResponse,
    })
  }

  reset = () => {
    this.setState({
      complete: false,
    })
  }

  showInactivePage(apiResponse) {
    ReactDOM.render(
      <AccountInactivePage
        activation={apiResponse.code}
        message={apiResponse.detail}
      />,
      document.getElementById("page-mount")
    )
  }

  render() {
    if (this.state.complete) {
      return <LinkSent callback={this.reset} user={this.state.complete} />
    }

    return (
      <RequestResetForm
        callback={this.complete}
        showInactivePage={this.showInactivePage}
      />
    )
  }
}
