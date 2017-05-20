import React from 'react'; // jshint ignore:line
import Button from 'misago/components/button'; // jshint ignore:line
import Form from 'misago/components/form';
import FormGroup from 'misago/components/form-group'; // jshint ignore:line
import ajax from 'misago/services/ajax';
import snackbar from 'misago/services/snackbar';

export default class extends Form {
  constructor(props) {
    super(props);

    this.state = {
      new_password: '',
      repeat_password: '',
      password: '',

      validators: {
        new_password: [],
        repeat_password: [],
        password: []
      },

      isLoading: false
    };
  }

  clean() {
    let errors = this.validate();
    let lengths = [
      this.state.new_password.trim().length,
      this.state.repeat_password.trim().length,
      this.state.password.trim().length
    ];

    if (lengths.indexOf(0) !== -1) {
      snackbar.error(gettext("Fill out all fields."));
      return false;
    }

    if (errors.new_password) {
      snackbar.error(errors.new_password[0]);
      return false;
    }

    if (this.state.new_password.trim() !== this.state.repeat_password.trim()) {
      snackbar.error(gettext("New passwords are different."));
      return false;
    }

    return true;
  }

  send() {
    return ajax.post(this.propsuser.api.change_password, {
      new_password: this.state.new_password,
      password: this.state.password
    });
  }

  handleSuccess(response) {
    this.setState({
      new_password: '',
      repeat_password: '',
      password: ''
    });

    snackbar.success(response.detail);
  }

  handleError(rejection) {
    if (rejection.status === 400) {
      if (rejection.new_password) {
        snackbar.error(rejection.new_password);
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
          <h3 className="panel-title">{gettext("Change password")}</h3>
        </div>
        <div className="panel-body">

          <FormGroup label={gettext("New password")} for="id_new_password">
            <input type="password" id="id_new_password" className="form-control"
                   disabled={this.state.isLoading}
                   onChange={this.bindInput('new_password')}
                   value={this.state.new_password} />
          </FormGroup>

          <FormGroup label={gettext("Repeat password")} for="id_repeat_password">
            <input type="password" id="id_repeat_password" className="form-control"
                   disabled={this.state.isLoading}
                   onChange={this.bindInput('repeat_password')}
                   value={this.state.repeat_password} />
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
            {gettext("Change password")}
          </Button>

        </div>
      </div>
    </form>;
    /* jshint ignore:end */
  }
}
