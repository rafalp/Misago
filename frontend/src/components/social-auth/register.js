/* jshint ignore:start */
import React from 'react';
import RegisterLegalFootnote from 'misago/components/RegisterLegalFootnote';
import Button from 'misago/components/button';
import Form from 'misago/components/form';
import FormGroup from 'misago/components/form-group';
import ajax from 'misago/services/ajax';
import snackbar from 'misago/services/snackbar';
import * as validators from 'misago/utils/validators';
import Header from './header';

export default class Register extends Form {
  constructor(props) {
    super(props);

    this.state = {
      email: props.email || '',
      emailProtected: !!props.email,
      username: props.username || '',

      errors: {},

      validators: {
        email: [
          validators.email()
        ],
        username: [
          validators.usernameContent()
        ]
      },

      isLoading: false
    };
  }

  clean() {
    let errors = this.validate();
    let lengths = [
      this.state.email.trim().length,
      this.state.username.trim().length
    ];

    if (lengths.indexOf(0) !== -1) {
      snackbar.error(gettext("Fill out all fields."));
      return false;
    }

    return true;
  }

  send() {
    return ajax.post(this.props.url, {
      email: this.state.email,
      username: this.state.username
    });
  }

  handleSuccess(response) {
    onRegistrationComplete(response);
  }

  handleError(rejection) {
    if (rejection.status === 200) {
      // We've entered "errored" state because response is HTML instead of exptected JSON
      const { onRegistrationComplete } = this.props;
      const { username } = this.state;
      onRegistrationComplete({ activation: 'active', step: 'done', username });
    } else if (rejection.status === 400) {
      const stateUpdate = { errors: rejection };
      if (rejection.email) {
        stateUpdate.emailProtected = false;
      }
      this.setState(stateUpdate);
    } else {
      snackbar.apiError(rejection);
    }
  }

  render() {
    const { backend_name } = this.props;
    const {
      email,
      emailProtected,
      username,
      isLoading
    } = this.state;

    let emailHelpText = null;
    if (emailProtected) {
      const emailHelpTextTpl = gettext("Your e-mail address has been verified by %(backend)s.");
      emailHelpText = interpolate(emailHelpTextTpl, { backend: backend_name }, true);
    }

    return (
      <div className="page page-social-auth page-social-sauth-register">
        <Header backendName={backend_name} />
        <div className="container">
          <div className="row">
            <div className="col-md-6 col-md-offset-3">
              <form onSubmit={this.handleSubmit}>
                <div className="panel panel-default panel-form">
                  <div className="panel-heading">
                    <h3 className="panel-title">{gettext("Complete your details")}</h3>
                  </div>
                  <div className="panel-body">
                    <FormGroup
                      for="id_username"
                      label={gettext("Username")}
                      validation={this.state.errors.username}
                    >
                      <input
                        type="text"
                        id="id_username"
                        className="form-control"
                        disabled={isLoading}
                        onChange={this.bindInput('username')}
                        value={username}
                      />
                    </FormGroup>
                    <FormGroup
                      for="id_email"
                      label={gettext("E-mail address")}
                      helpText={emailHelpText}
                      validation={emailProtected ? null : this.state.errors.email}
                    >
                      <input
                        type="email"
                        id="id_email"
                        className="form-control"
                        disabled={isLoading || emailProtected}
                        onChange={this.bindInput('email')}
                        value={email}
                      />
                    </FormGroup>
                    <RegisterLegalFootnote />
                  </div>
                  <div className="panel-footer">
                    <Button className="btn-primary" loading={this.state.isLoading}>
                      {gettext("Sign in")}
                    </Button>
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    );
  }
}