import React from 'react'; // jshint ignore:line
import Button from 'misago/components/button'; // jshint ignore:line
import Form from 'misago/components/form';
import FormGroup from 'misago/components/form-group'; // jshint ignore:line
import ajax from 'misago/services/ajax';
import snackbar from 'misago/services/snackbar';
import * as validators from 'misago/utils/validators';

export default class extends Form {
  constructor(props) {
    super(props);

    this.state = {
      new_email: '',
      password: '',

      validators: {
        new_email: [
          validators.email()
        ],
        password: []
      },

      isLoading: false
    };
  }

  clean() {
    let errors = this.validate();
    let lengths = [
      this.state.new_email.trim().length,
      this.state.password.trim().length
    ];

    if (lengths.indexOf(0) !== -1) {
      snackbar.error(gettext("Fill out all fields."));
      return false;
    }

    if (errors.new_email) {
      snackbar.error(errors.new_email[0]);
      return false;
    }

    return true;
  }

  send() {
    return ajax.post(this.props.user.api_url.change_email, {
      new_email: this.state.new_email,
      password: this.state.password,
    });
  }

  handleSuccess(response) {
    this.setState({
      new_email: '',
      password: ''
    });

    snackbar.success(response.detail);
  }

  handleError(rejection) {
    if (rejection.status === 400) {
      if (rejection.new_email) {
        snackbar.error(rejection.new_email);
      } else {
        snackbar.error(rejection.password);
      }
    } else {
      snackbar.apiError(rejection);
    }
  }

  render() {
    /* jshint ignore:start */
    return <form onSubmit={this.handleSubmit}>
      <input type="type" style={{display: 'none'}} />
      <input type="password" style={{display: 'none'}} />
      <div className="panel panel-default panel-form">
        <div className="panel-heading">
          <h3 className="panel-title">{gettext("Change e-mail address")}</h3>
        </div>
        <div className="panel-body">

          <FormGroup label={gettext("New e-mail")} for="id_new_email">
            <input type="text" id="id_new_email" className="form-control"
                   disabled={this.state.isLoading}
                   onChange={this.bindInput('new_email')}
                   value={this.state.new_email} />
          </FormGroup>

          <hr />

          <FormGroup label={gettext("Your current password")} for="id_password">
            <input type="password" id="id_password" className="form-control"
                   disabled={this.state.isLoading}
                   onChange={this.bindInput('password')}
                   value={this.state.password} />
          </FormGroup>

        </div>
        <div className="panel-footer">

          <Button className="btn-primary" loading={this.state.isLoading}>
            {gettext("Change e-mail")}
          </Button>

        </div>
      </div>
    </form>;
    /* jshint ignore:end */
  }
}