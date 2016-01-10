import React from 'react'; // jshint ignore:line
import ReactDOM from 'react-dom'; // jshint ignore:line
import misago from 'misago/index';
import Button from 'misago/components/button'; // jshint ignore:line
import Form from 'misago/components/form';
import ajax from 'misago/services/ajax';
import snackbar from 'misago/services/snackbar';
import * as validators from 'misago/utils/validators';
import showBannedPage from 'misago/utils/banned-page';

export class RequestResetForm extends Form {
  constructor(props) {
    super(props);

    this.state = {
      'isLoading': false,

      'email': '',

      'validators': {
        'email': [
          validators.email()
        ]
      }
    };
  }

  clean() {
    if (this.isValid()) {
      return true;
    } else {
      snackbar.error(gettext("Enter a valid email address."));
      return false;
    }
  }

  send() {
    return ajax.post(misago.get('SEND_PASSWORD_RESET_API'), {
      'email': this.state.email
    });
  }

  handleSuccess(apiResponse) {
    this.props.callback(apiResponse);
  }

  handleError(rejection) {
    if (['inactive_user', 'inactive_admin'].indexOf(rejection.code) > -1) {
      this.props.showInactivePage(rejection);
    } else if (rejection.status === 403 && rejection.ban) {
      showBannedPage(rejection.ban);
    } else {
      snackbar.apiError(rejection);
    }
  }

  render() {
    /* jshint ignore:start */
    return <div className="well well-form well-form-request-password-reset">
      <form onSubmit={this.handleSubmit}>
        <div className="form-group">
          <div className="control-input">

            <input type="text" className="form-control"
                   placeholder={gettext("Your e-mail address")}
                   disabled={this.state.isLoading}
                   onChange={this.bindInput('email')}
                   value={this.state.email} />

          </div>
        </div>

        <Button className="btn-primary btn-block"
                loading={this.state.isLoading}>
          {gettext("Send link")}
        </Button>

      </form>
    </div>;
    /* jshint ignore:end */
  }
}

export class LinkSent extends React.Component {
  getMessage() {
    return interpolate(gettext("Reset password link was sent to %(email)s"), {
      email: this.props.user.email
    }, true);
  }

  render() {
    /* jshint ignore:start */
    return <div className="well well-form well-form-request-password-reset well-done">
      <div className="done-message">
        <div className="message-icon">
          <span className="material-icon">
            check
          </span>
        </div>
        <div className="message-body">
          <p>
            {this.getMessage()}
          </p>
        </div>
        <button type="button" className="btn btn-primary btn-block"
                onClick={this.props.callback}>
          {gettext("Request another link")}
        </button>
      </div>
    </div>;
    /* jshint ignore:end */
  }
}

export class AccountInactivePage extends React.Component {
  getActivateButton() {
    if (this.props.activation === 'inactive_user') {
      /* jshint ignore:start */
      return <p>
        <a href={misago.get('REQUEST_ACTIVATION_URL')}>
          {gettext("Activate your account.")}
        </a>
      </p>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  render() {
    /* jshint ignore:start */
    return <div className="page page-message page-message-info page-forgotten-password-inactive">
      <div className="container">
        <div className="message-panel">

          <div className="message-icon">
            <span className="material-icon">
              info_outline
            </span>
          </div>

          <div className="message-body">
            <p className="lead">
              {gettext("Your account is inactive.")}
            </p>
            <p>
              {this.props.message}
            </p>
            {this.getActivateButton()}
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
  complete = (apiResponse) => {
    this.setState({
      complete: apiResponse
    });
  }

  reset = () => {
    this.setState({
      complete: false
    });
  }

  showInactivePage(apiResponse) {
    ReactDOM.render(
      <AccountInactivePage activation={apiResponse.code}
                           message={apiResponse.detail} />,
      document.getElementById('page-mount')
    );
  }
  /* jshint ignore:end */

  render() {
    /* jshint ignore:start */
    if (this.state.complete) {
      return <LinkSent user={this.state.complete} callback={this.reset} />;
    } else {
      return <RequestResetForm callback={this.complete}
                               showInactivePage={this.showInactivePage} />;
    };
    /* jshint ignore:end */
  }
}