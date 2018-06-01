import React from 'react'; // jshint ignore:line
import misago from 'misago/index';
import Button from 'misago/components/button'; // jshint ignore:line
import Form from 'misago/components/form';
import StartSocialAuth from 'misago/components/StartSocialAuth'; // jshint ignore:line
import ajax from 'misago/services/ajax';
import modal from 'misago/services/modal';
import snackbar from 'misago/services/snackbar';
import showBannedPage from 'misago/utils/banned-page';

export default class extends Form {
  constructor(props) {
    super(props);

    this.state = {
      'isLoading': false,
      'showActivation': false,

      'username': '',
      'password': '',

      'validators': {
        'username': [],
        'password': []
      }
    };
  }

  clean() {
    if (!this.isValid()) {
      snackbar.error(gettext("Fill out both fields."));
      return false;
    } else {
      return true;
    }
  }

  send() {
    return ajax.post(misago.get('AUTH_API'), {
      'username': this.state.username,
      'password': this.state.password
    });
  }

  handleSuccess() {
    let form = $('#hidden-login-form');

    form.append('<input type="text" name="username" />');
    form.append('<input type="password" name="password" />');

    // fill out form with user credentials and submit it, this will tell
    // Misago to redirect user back to right page, and will trigger browser's
    // key ring feature
    form.find('input[type="hidden"]').val(ajax.getCsrfToken());
    form.find('input[name="redirect_to"]').val(window.location.pathname);
    form.find('input[name="username"]').val(this.state.username);
    form.find('input[name="password"]').val(this.state.password);
    form.submit();

    // keep form loading
    this.setState({
      'isLoading': true
    });
  }

  handleError(rejection) {
    if (rejection.status === 400) {
      if (rejection.code === 'inactive_admin') {
        snackbar.info(rejection.detail);
      } else if (rejection.code === 'inactive_user') {
        snackbar.info(rejection.detail);
        this.setState({
          'showActivation': true
        });
      } else if (rejection.code === 'banned') {
        showBannedPage(rejection.detail);
        modal.hide();
      } else {
        snackbar.error(rejection.detail);
      }
    } else if (rejection.status === 403 && rejection.ban) {
      showBannedPage(rejection.ban);
      modal.hide();
    } else {
      snackbar.apiError(rejection);
    }
  }

  getActivationButton() {
    if (!this.state.showActivation) return null;

    /* jshint ignore:start */
    return (
      <a
        className="btn btn-success btn-block"
        href={misago.get('REQUEST_ACTIVATION_URL')}
      >
        {gettext("Activate account")}
      </a>
    );
    /* jshint ignore:end */
  }

  render() {
    /* jshint ignore:start */
    return (
      <div
        className="modal-dialog modal-sm modal-sign-in"
        role="document"
      >
        <div className="modal-content">
          <div className="modal-header">
            <button
              aria-label={gettext("Close")}
              className="close"
              data-dismiss="modal"
              type="button"
            >
              <span aria-hidden="true">&times;</span>
            </button>
            <h4 className="modal-title">{gettext("Sign in")}</h4>
          </div>
          <form onSubmit={this.handleSubmit}>
            <div className="modal-body">

              <StartSocialAuth
                buttonLabel={gettext("Sign in with %(site)s")}
                formLabel={gettext("Or use your forum account:")}
                labelClassName="text-center"
              />

              <div className="form-group">
                <div className="control-input">
                  <input
                    className="form-control input-lg"
                    disabled={this.state.isLoading}
                    id="id_username"
                    onChange={this.bindInput('username')}
                    placeholder={gettext("Username or e-mail")}
                    type="text"
                    value={this.state.username}
                  />
                </div>
              </div>

              <div className="form-group">
                <div className="control-input">
                  <input
                    className="form-control input-lg"
                    disabled={this.state.isLoading}
                    id="id_password"
                    onChange={this.bindInput('password')}
                    placeholder={gettext("Password")}
                    type="password"
                    value={this.state.password}
                  />
                </div>
              </div>

            </div>
            <div className="modal-footer">
              {this.getActivationButton()}
              <Button
                className="btn-primary btn-block"
                loading={this.state.isLoading}
              >
                {gettext("Sign in")}
              </Button>
              <a
                className="btn btn-default btn-block"
                href={misago.get('FORGOTTEN_PASSWORD_URL')}
              >
                 {gettext("Forgot password?")}
              </a>
            </div>
          </form>
        </div>
      </div>
    );
    /* jshint ignore:end */
  }
}
