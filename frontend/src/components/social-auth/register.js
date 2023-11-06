import React from "react"
import misago from "misago"
import RegisterLegalFootnote from "misago/components/RegisterLegalFootnote"
import Button from "misago/components/button"
import Form from "misago/components/form"
import FormGroup from "misago/components/form-group"
import ajax from "misago/services/ajax"
import snackbar from "misago/services/snackbar"
import * as validators from "misago/utils/validators"
import PageContainer from "../PageContainer"
import Header from "./header"

export default class Register extends Form {
  constructor(props) {
    super(props)

    const formValidators = {
      email: [validators.email()],
      username: [validators.usernameContent()],
    }

    if (!!misago.get("TERMS_OF_SERVICE_ID")) {
      formValidators.termsOfService = [validators.requiredTermsOfService()]
    }

    if (!!misago.get("PRIVACY_POLICY_ID")) {
      formValidators.privacyPolicy = [validators.requiredPrivacyPolicy()]
    }

    this.state = {
      email: props.email || "",
      emailProtected: !!props.email,
      username: props.username || "",

      termsOfService: null,
      privacyPolicy: null,

      validators: formValidators,
      errors: {},

      isLoading: false,
    }
  }

  clean() {
    let errors = this.validate()
    let lengths = [
      this.state.email.trim().length,
      this.state.username.trim().length,
    ]

    if (lengths.indexOf(0) !== -1) {
      snackbar.error(pgettext("social auth form", "Fill out all fields."))
      return false
    }

    const { validators } = this.state

    const checkTermsOfService = !!misago.get("TERMS_OF_SERVICE_ID")
    if (checkTermsOfService && this.state.termsOfService === null) {
      snackbar.error(validators.termsOfService[0](null))
      return false
    }

    const checkPrivacyPolicy = !!misago.get("PRIVACY_POLICY_ID")
    if (checkPrivacyPolicy && this.state.privacyPolicy === null) {
      snackbar.error(validators.privacyPolicy[0](null))
      return false
    }

    return true
  }

  send() {
    return ajax.post(this.props.url, {
      email: this.state.email,
      username: this.state.username,
      terms_of_service: this.state.termsOfService,
      privacy_policy: this.state.privacyPolicy,
    })
  }

  handleSuccess(response) {
    const { onRegistrationComplete } = this.props
    onRegistrationComplete(response)
  }

  handleError(rejection) {
    if (rejection.status === 200) {
      // We've entered "errored" state because response is HTML instead of exptected JSON
      const { onRegistrationComplete } = this.props
      const { username } = this.state
      onRegistrationComplete({ activation: "active", step: "done", username })
    } else if (rejection.status === 400) {
      const stateUpdate = { errors: rejection }
      if (rejection.email) {
        stateUpdate.emailProtected = false
      }
      this.setState(stateUpdate)
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
    const { backend_name } = this.props
    const { email, emailProtected, username, isLoading } = this.state

    let emailHelpText = null
    if (emailProtected) {
      const emailHelpTextTpl = pgettext(
        "social auth form",
        "Your e-mail address has been verified by %(backend)s."
      )
      emailHelpText = interpolate(
        emailHelpTextTpl,
        { backend: backend_name },
        true
      )
    }

    return (
      <div className="page page-social-auth page-social-auth-register">
        <Header backendName={backend_name} />
        <PageContainer>
          <div className="row">
            <div className="col-md-6 col-md-offset-3">
              <form onSubmit={this.handleSubmit}>
                <div className="panel panel-default panel-form">
                  <div className="panel-heading">
                    <h3 className="panel-title">
                      {pgettext(
                        "social auth form title",
                        "Complete your account"
                      )}
                    </h3>
                  </div>
                  <div className="panel-body">
                    <FormGroup
                      for="id_username"
                      label={pgettext("social auth form field", "Username")}
                      validation={this.state.errors.username}
                    >
                      <input
                        type="text"
                        id="id_username"
                        className="form-control"
                        disabled={isLoading}
                        onChange={this.bindInput("username")}
                        value={username}
                      />
                    </FormGroup>
                    <FormGroup
                      for="id_email"
                      label={pgettext(
                        "social auth form field",
                        "E-mail address"
                      )}
                      helpText={emailHelpText}
                      validation={
                        emailProtected ? null : this.state.errors.email
                      }
                    >
                      <input
                        type="email"
                        id="id_email"
                        className="form-control"
                        disabled={isLoading || emailProtected}
                        onChange={this.bindInput("email")}
                        value={email}
                      />
                    </FormGroup>
                    <RegisterLegalFootnote
                      errors={this.state.errors}
                      privacyPolicy={this.state.privacyPolicy}
                      termsOfService={this.state.termsOfService}
                      onPrivacyPolicyChange={this.handlePrivacyPolicyChange}
                      onTermsOfServiceChange={this.handleTermsOfServiceChange}
                    />
                  </div>
                  <div className="panel-footer">
                    <Button
                      className="btn-primary"
                      loading={this.state.isLoading}
                    >
                      {pgettext("social auth form btn", "Sign in")}
                    </Button>
                  </div>
                </div>
              </form>
            </div>
          </div>
        </PageContainer>
      </div>
    )
  }
}
