import React from "react"
import Button from "misago/components/button"
import Form from "misago/components/form"
import FormGroup from "misago/components/form-group"
import PasswordStrength from "misago/components/password-strength"
import RegisterLegalFootnote from "misago/components/RegisterLegalFootnote"
import StartSocialAuth from "misago/components/StartSocialAuth"
import misago from "misago"
import ajax from "misago/services/ajax"
import auth from "misago/services/auth"
import captcha from "misago/services/captcha"
import modal from "misago/services/modal"
import snackbar from "misago/services/snackbar"
import showBannedPage from "misago/utils/banned-page"
import * as validators from "misago/utils/validators"

export class RegisterForm extends Form {
  constructor(props) {
    super(props)

    const { username, password } = this.props.criteria

    let passwordMinLength = 0
    password.forEach((item) => {
      if (item.name === "MinimumLengthValidator") {
        passwordMinLength = item.min_length
      }
    })

    const formValidators = {
      username: [
        validators.usernameContent(),
        validators.usernameMinLength(username.min_length),
        validators.usernameMaxLength(username.max_length),
      ],
      email: [validators.email()],
      password: [validators.passwordMinLength(passwordMinLength)],
      captcha: captcha.validator(),
    }

    if (!!misago.get("TERMS_OF_SERVICE_ID")) {
      formValidators.termsOfService = [validators.requiredTermsOfService()]
    }

    if (!!misago.get("PRIVACY_POLICY_ID")) {
      formValidators.privacyPolicy = [validators.requiredPrivacyPolicy()]
    }

    this.state = {
      isLoading: false,

      username: "",
      email: "",
      password: "",
      captcha: "",

      termsOfService: null,
      privacyPolicy: null,

      validators: formValidators,
      errors: {},
    }
  }

  clean() {
    if (this.isValid()) {
      return true
    } else {
      snackbar.error(gettext("Form contains errors."))
      this.setState({
        errors: this.validate(),
      })
      return false
    }
  }

  send() {
    return ajax.post(misago.get("USERS_API"), {
      username: this.state.username,
      email: this.state.email,
      password: this.state.password,
      captcha: this.state.captcha,
      terms_of_service: this.state.termsOfService,
      privacy_policy: this.state.privacyPolicy,
    })
  }

  handleSuccess(apiResponse) {
    this.props.callback(apiResponse)
  }

  handleError(rejection) {
    if (rejection.status === 400) {
      this.setState({
        errors: Object.assign({}, this.state.errors, rejection),
      })

      if (rejection.__all__ && rejection.__all__.length > 0) {
        snackbar.error(rejection.__all__[0])
      } else {
        snackbar.error(gettext("Form contains errors."))
      }
    } else if (rejection.status === 403 && rejection.ban) {
      showBannedPage(rejection.ban)
      modal.hide()
    } else {
      snackbar.apiError(rejection)
    }
  }

  handlePrivacyPolicyChange = (event) => {
    const value = event.target.value
    this.handleToggleAgreement("privacyPolicy", value)
  }

  handleTermsOfServiceChange = (event) => {
    const value = event.target.value
    this.handleToggleAgreement("termsOfService", value)
  }

  handleToggleAgreement = (agreement, value) => {
    this.setState((prevState, props) => {
      if (prevState[agreement] === null) {
        const errors = { ...prevState.errors, [agreement]: null }
        return { errors, [agreement]: value }
      }

      const validator = this.state.validators[agreement][0]
      const errors = { ...prevState.errors, [agreement]: [validator(null)] }
      return { errors, [agreement]: null }
    })
  }

  render() {
    return (
      <div className="modal-dialog modal-register" role="document">
        <div className="modal-content">
          <div className="modal-header">
            <button
              type="button"
              className="close"
              data-dismiss="modal"
              aria-label={pgettext("modal", "Close")}
            >
              <span aria-hidden="true">&times;</span>
            </button>
            <h4 className="modal-title">
              {pgettext("register modal title", "Register")}
            </h4>
          </div>
          <form onSubmit={this.handleSubmit}>
            <input type="type" style={{ display: "none" }} />
            <input type="password" style={{ display: "none" }} />
            <div className="modal-body">
              <StartSocialAuth
                buttonClassName="col-xs-12 col-sm-6"
                buttonLabel={pgettext(
                  "register modal field",
                  "Join with %(site)s"
                )}
                formLabel={pgettext(
                  "register modal field",
                  "Or create forum account:"
                )}
              />

              <FormGroup
                label={pgettext("register modal field", "Username")}
                for="id_username"
                validation={this.state.errors.username}
              >
                <input
                  type="text"
                  id="id_username"
                  className="form-control"
                  aria-describedby="id_username_status"
                  disabled={this.state.isLoading}
                  onChange={this.bindInput("username")}
                  value={this.state.username}
                />
              </FormGroup>

              <FormGroup
                label={pgettext("register modal field", "E-mail")}
                for="id_email"
                validation={this.state.errors.email}
              >
                <input
                  type="text"
                  id="id_email"
                  className="form-control"
                  aria-describedby="id_email_status"
                  disabled={this.state.isLoading}
                  onChange={this.bindInput("email")}
                  value={this.state.email}
                />
              </FormGroup>

              <FormGroup
                label={pgettext("register modal field", "Password")}
                for="id_password"
                validation={this.state.errors.password}
                extra={
                  <PasswordStrength
                    password={this.state.password}
                    inputs={[this.state.username, this.state.email]}
                  />
                }
              >
                <input
                  type="password"
                  id="id_password"
                  className="form-control"
                  aria-describedby="id_password_status"
                  disabled={this.state.isLoading}
                  onChange={this.bindInput("password")}
                  value={this.state.password}
                />
              </FormGroup>

              {captcha.component({
                form: this,
              })}

              <RegisterLegalFootnote
                errors={this.state.errors}
                privacyPolicy={this.state.privacyPolicy}
                termsOfService={this.state.termsOfService}
                onPrivacyPolicyChange={this.handlePrivacyPolicyChange}
                onTermsOfServiceChange={this.handleTermsOfServiceChange}
              />
            </div>
            <div className="modal-footer">
              <button
                className="btn btn-default"
                data-dismiss="modal"
                disabled={this.state.isLoading}
                type="button"
              >
                {pgettext("register modal btn", "Cancel")}
              </button>
              <Button className="btn-primary" loading={this.state.isLoading}>
                {pgettext("register modal btn", "Register account")}
              </Button>
            </div>
          </form>
        </div>
      </div>
    )
  }
}

export class RegisterComplete extends React.Component {
  getLead() {
    if (this.props.activation === "user") {
      return pgettext(
        "account activation required",
        "%(username)s, your account has been created but you need to activate it before you will be able to sign in."
      )
    } else if (this.props.activation === "admin") {
      return pgettext(
        "account activation required",
        "%(username)s, your account has been created but the site administrator will have to activate it before you will be able to sign in."
      )
    }
  }

  getSubscript() {
    if (this.props.activation === "user") {
      return pgettext(
        "account activation required",
        "We have sent an e-mail to %(email)s with link that you have to click to activate your account."
      )
    } else if (this.props.activation === "admin") {
      return pgettext(
        "account activation required",
        "We will send an e-mail to %(email)s when this takes place."
      )
    }
  }

  render() {
    return (
      <div
        className="modal-dialog modal-message modal-register"
        role="document"
      >
        <div className="modal-content">
          <div className="modal-header">
            <button
              type="button"
              className="close"
              data-dismiss="modal"
              aria-label={pgettext("modal", "Close")}
            >
              <span aria-hidden="true">&times;</span>
            </button>
            <h4 className="modal-title">
              {pgettext("register modal title", "Registration complete")}
            </h4>
          </div>
          <div className="modal-body">
            <div className="message-icon">
              <span className="material-icon">info_outline</span>
            </div>
            <div className="message-body">
              <p className="lead">
                {interpolate(
                  this.getLead(),
                  { username: this.props.username },
                  true
                )}
              </p>
              <p>
                {interpolate(
                  this.getSubscript(),
                  { email: this.props.email },
                  true
                )}
              </p>
              <button
                className="btn btn-default"
                data-dismiss="modal"
                type="button"
              >
                {pgettext("register modal dismiss", "Ok")}
              </button>
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

  completeRegistration = (apiResponse) => {
    if (apiResponse.activation === "active") {
      modal.hide()
      auth.signIn(apiResponse)
    } else {
      this.setState({
        complete: apiResponse,
      })
    }
  }

  render() {
    if (this.state.complete) {
      return (
        <RegisterComplete
          activation={this.state.complete.activation}
          email={this.state.complete.email}
          username={this.state.complete.username}
        />
      )
    }

    return <RegisterForm callback={this.completeRegistration} {...this.props} />
  }
}
