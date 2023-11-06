import React from "react"
import misago from "misago/index"
import Button from "misago/components/button"
import Form from "misago/components/form"
import ajax from "misago/services/ajax"
import snackbar from "misago/services/snackbar"
import * as validators from "misago/utils/validators"
import showBannedPage from "misago/utils/banned-page"

export class RequestLinkForm extends Form {
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
        pgettext(
          "request activation link form",
          "Enter a valid e-mail address."
        )
      )
      return false
    }
  }

  send() {
    return ajax.post(misago.get("SEND_ACTIVATION_API"), {
      email: this.state.email,
    })
  }

  handleSuccess(apiResponse) {
    this.props.callback(apiResponse)
  }

  handleError(rejection) {
    if (["already_active", "inactive_admin"].indexOf(rejection.code) > -1) {
      snackbar.info(rejection.detail)
    } else if (rejection.status === 403 && rejection.ban) {
      showBannedPage(rejection.ban)
    } else {
      snackbar.apiError(rejection)
    }
  }

  render() {
    return (
      <div className="well well-form well-form-request-activation-link">
        <form onSubmit={this.handleSubmit}>
          <div className="form-group">
            <div className="control-input">
              <input
                type="text"
                className="form-control"
                placeholder={pgettext(
                  "request activation link form field",
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
            {pgettext("request activation link form btn", "Send link")}
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
        "request activation link form",
        "Activation link was sent to %(email)s"
      ),
      {
        email: this.props.user.email,
      },
      true
    )
  }

  render() {
    return (
      <div className="well well-form well-form-request-activation-link well-done">
        <div className="done-message">
          <div className="message-icon">
            <span className="material-icon">check</span>
          </div>
          <div className="message-body">
            <p>{this.getMessage()}</p>
          </div>
          <button
            className="btn btn-primary btn-block"
            type="button"
            onClick={this.props.callback}
          >
            {pgettext(
              "request activation link form btn",
              "Request another link"
            )}
          </button>
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

  render() {
    if (this.state.complete) {
      return <LinkSent user={this.state.complete} callback={this.reset} />
    } else {
      return <RequestLinkForm callback={this.complete} />
    }
  }
}
