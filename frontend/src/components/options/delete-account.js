/* jshint ignore:start */
import React from 'react';
import Button from 'misago/components/button'; // jshint ignore:line
import ajax from 'misago/services/ajax';
import title from 'misago/services/page-title';
import snackbar from 'misago/services/snackbar';
import store from 'misago/services/store';
import misago from 'misago';

export default class extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      isLoading: false,
      password: '',
    };
  }

  componentDidMount() {
    title.set({
      title: gettext("Delete account"),
      parent: gettext("Change your options")
    });
  }

  onPasswordChange = (event) => {
    this.setState({ password: event.target.value });
  }

  handleSubmit = (event) => {
    event.preventDefault();

    const { isLoading, password } = this.state;
    const { user } = this.props;

    if (password.length == 0) {
      snackbar.error(gettext("Enter your password to confirm account deletion."));
      return false;
    }

    if (isLoading) return false;
    this.setState({ isLoading: true });

    ajax.post(user.api.delete, { password }).then(
      (success) => {
        window.location.href = misago.get('MISAGO_PATH');
      },
      (rejection) => {
        this.setState({ isLoading: false });
        if (rejection.password) {
          snackbar.error(rejection.password[0]);
        } else {
          snackbar.apiError(rejection)
        }
      }
    );
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <div className="panel panel-danger panel-form">
          <div className="panel-heading">
            <h3 className="panel-title">{gettext("Delete account")}</h3>
          </div>
          <div className="panel-body">

            <p className="lead">
              {gettext("You are going to delete your account. This action is nonreversible, and will result in following data being deleted:")}
            </p>

            <p>- {gettext("Stored IP addresses associated with content that you have posted will be deleted.")}</p>
            <p>- {gettext("Your username will become available for other user to rename to or for new user to register their account with.")}</p>
            <p>- {gettext("Your e-mail will become available for use in new account registration.")}</p>

            <hr/>

            <p>{gettext("All your posted content will NOT be deleted, but username associated with it will be changed to one shared by all deleted accounts.")}</p>

          </div>
          <div className="panel-footer">

            <div className="input-group">
              <input 
                className="form-control"
                disabled={this.state.isLoading}
                name="password-confirmation"
                type="password"
                placeholder={gettext("Enter your password to confirm account deletion.")}
                value={this.state.password}
                onChange={this.onPasswordChange}
              />
              <span className="input-group-btn">
                <Button className="btn-danger" loading={this.state.isLoading}>
                  {gettext("Delete my account")}
                </Button>
              </span>
            </div>

          </div>
        </div>
      </form>
    );
  }
}