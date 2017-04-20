import React from 'react';
import Button from 'misago/components/button'; // jshint ignore:line
import Form from 'misago/components/form';
import FormGroup from 'misago/components/form-group'; // jshint ignore:line
import PasswordStrength from 'misago/components/password-strength'; // jshint ignore:line
import misago from 'misago';
import ajax from 'misago/services/ajax';
import auth from 'misago/services/auth'; // jshint ignore:line
import captcha from 'misago/services/captcha';
import modal from 'misago/services/modal';
import snackbar from 'misago/services/snackbar';
import showBannedPage from 'misago/utils/banned-page';
import * as validators from 'misago/utils/validators';

export class RegisterForm extends Form {
  constructor(props) {
    super(props);

    const { username, password } = this.props.criteria;

    let passwordMinLength = 0;
    password.forEach((item) => {
      if (item.name === 'MinimumLengthValidator') {
        passwordMinLength = item.min_length;
      }
    });

    this.state = {
      isLoading: false,

      username: '',
      email: '',
      password: '',
      captcha: '',

      validators: {
        username: [
          validators.usernameContent(),
          validators.usernameMinLength(username.min_length),
          validators.usernameMaxLength(username.max_length)
        ],
        email: [
          validators.email()
        ],
        password: [
          validators.passwordMinLength(passwordMinLength)
        ],
        captcha: captcha.validator()
      },

      errors: {}
    };
  }

  clean() {
    if (this.isValid()) {
      return true;
    } else {
      snackbar.error(gettext("Form contains errors."));
      this.setState({
        errors: this.validate()
      });
      return false;
    }
  }

  send() {
    return ajax.post(misago.get('USERS_API'), {
      username: this.state.username,
      email: this.state.email,
      password: this.state.password,
      captcha: this.state.captcha
    });
  }

  handleSuccess(apiResponse) {
    this.props.callback(apiResponse);
  }

  handleError(rejection) {
    if (rejection.status === 400) {
      this.setState({
        'errors': Object.assign({}, this.state.errors, rejection)
      });

      if (rejection.__all__ && rejection.__all__.length > 0) {
        snackbar.error(rejection.__all__[0]);
      } else {
        snackbar.error(gettext("Form contains errors."));
      }
    } else if (rejection.status === 403 && rejection.ban) {
      showBannedPage(rejection.ban);
      modal.hide();
    } else {
      snackbar.apiError(rejection);
    }
  }

  getLegalFootNote() {
    if (misago.get('TERMS_OF_SERVICE_URL')) {
      /* jshint ignore:start */
      return <a href={misago.get('TERMS_OF_SERVICE_URL')}
                target="_blank">
        {gettext("By registering you agree to site's terms and conditions.")}
      </a>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  render() {
    /* jshint ignore:start */
    return <div className="modal-dialog modal-register" role="document">
      <div className="modal-content">
        <div className="modal-header">
          <button type="button" className="close" data-dismiss="modal"
                  aria-label={gettext("Close")}>
            <span aria-hidden="true">&times;</span>
          </button>
          <h4 className="modal-title">{gettext("Register")}</h4>
        </div>
        <form onSubmit={this.handleSubmit}>
          <input type="type" style={{display: 'none'}} />
          <input type="password" style={{display: 'none'}} />
          <div className="modal-body">

            <FormGroup label={gettext("Username")} for="id_username"
                       validation={this.state.errors.username}>
              <input type="text" id="id_username" className="form-control"
                     aria-describedby="id_username_status"
                     disabled={this.state.isLoading}
                     onChange={this.bindInput('username')}
                     value={this.state.username} />
            </FormGroup>

            <FormGroup label={gettext("E-mail")} for="id_email"
                       validation={this.state.errors.email}>
              <input type="text" id="id_email" className="form-control"
                     aria-describedby="id_email_status"
                     disabled={this.state.isLoading}
                     onChange={this.bindInput('email')}
                     value={this.state.email} />
            </FormGroup>

            <FormGroup label={gettext("Password")} for="id_password"
                       validation={this.state.errors.password}
                       extra={<PasswordStrength password={this.state.password}
                                                inputs={[
                                                  this.state.username,
                                                  this.state.email
                                                ]} />} >
              <input type="password" id="id_password" className="form-control"
                     aria-describedby="id_password_status"
                     disabled={this.state.isLoading}
                     onChange={this.bindInput('password')}
                     value={this.state.password} />
            </FormGroup>

            {captcha.component({
              form: this,
            })}

          </div>
          <div className="modal-footer">
            <Button className="btn-primary" loading={this.state.isLoading}>
              {gettext("Register account")}
            </Button>
            {this.getLegalFootNote()}
          </div>
        </form>
      </div>
    </div>;
    /* jshint ignore:end */
  }
}

export class RegisterComplete extends React.Component {
  getLead() {
    if (this.props.activation === 'user') {
      return gettext("%(username)s, your account has been created but you need to activate it before you will be able to sign in.");
    } else if (this.props.activation === 'admin') {
      return gettext("%(username)s, your account has been created but board administrator will have to activate it before you will be able to sign in.");
    }
  }

  getSubscript() {
    if (this.props.activation === 'user') {
      return gettext("We have sent an e-mail to %(email)s with link that you have to click to activate your account.");
    } else if (this.props.activation === 'admin') {
      return gettext("We will send an e-mail to %(email)s when this takes place.");
    }
  }

  render() {
    /* jshint ignore:start */
    return <div className="modal-dialog modal-message modal-register"
                role="document">
      <div className="modal-content">
        <div className="modal-header">
          <button type="button" className="close" data-dismiss="modal"
                  aria-label={gettext("Close")}>
            <span aria-hidden="true">&times;</span>
          </button>
          <h4 className="modal-title">{gettext("Registration complete")}</h4>
        </div>
        <div className="modal-body">
          <div className="message-icon">
            <span className="material-icon">
              info_outline
            </span>
          </div>
          <div className="message-body">
            <p className="lead">
              {interpolate(
                this.getLead(),
                {'username': this.props.username}, true)}
            </p>
            <p>
              {interpolate(
                this.getSubscript(),
                {'email': this.props.email}, true)}
            </p>
          </div>
        </div>
      </div>
    </div>;
    /* jshint ignore:end */
  }
}

export default class extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      complete: false
    };
  }

  /* jshint ignore:start */
  completeRegistration = (apiResponse) => {
    if (apiResponse.activation === 'active') {
      modal.hide();
      auth.signIn(apiResponse);
    } else {
      this.setState({
        complete: apiResponse
      });
    }
  };
  /* jshint ignore:end */

  render() {
    /* jshint ignore:start */
    if (this.state.complete) {
      return <RegisterComplete activation={this.state.complete.activation}
                               username={this.state.complete.username}
                               email={this.state.complete.email} />;
    } else {
      return (
        <RegisterForm
          callback={this.completeRegistration}
          {...this.props}
        />
      );
    }
    /* jshint ignore:end */
  }
}
