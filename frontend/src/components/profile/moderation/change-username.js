import React from 'react'; // jshint ignore:line
import Button from 'misago/components/button'; // jshint ignore:line
import Form from 'misago/components/form';
import FormGroup from 'misago/components/form-group'; // jshint ignore:line
import Loader from 'misago/components/modal-loader'; // jshint ignore:line
import ModalMessage from 'misago/components/modal-message'; // jshint ignore:line
import { addNameChange } from 'misago/reducers/username-history'; // jshint ignore:line
import { updateUsername } from 'misago/reducers/users'; // jshint ignore:line
import ajax from 'misago/services/ajax';
import snackbar from 'misago/services/snackbar';
import store from 'misago/services/store';
import * as validators from 'misago/utils/validators';

export default class extends Form {
  constructor(props) {
    super(props);

    this.state = {
      isLoaded: false,
      isLoading: false,
      error: null,

      username: '',
      validators: {
        username: [
          validators.usernameContent()
        ]
      }
    };
  }

  componentDidMount() {
    ajax.get(this.props.profile.api_url.moderate_username).then(() => {
      this.setState({
        isLoaded: true
      });
    }, (rejection) => {
      this.setState({
        isLoaded: true,
        error: rejection.detail
      });
    });
  }

  clean() {
    if (this.isValid()) {
      return true;
    } else {
      snackbar.error(this.validate().username[0]);
      return false;
    }
  }

  send() {
    return ajax.post(this.props.profile.api_url.moderate_username, {
      username: this.state.username
    });
  }

  handleSuccess(apiResponse) {
    this.setState({
      username: ''
    });

    store.dispatch(addNameChange(
      apiResponse, this.props.profile, this.props.user));
    store.dispatch(updateUsername(
      this.props.profile, apiResponse.username, apiResponse.slug));

    snackbar.success(gettext("Username has been changed."));
  }

  getFormBody() {
    /* jshint ignore:start */
    return <form onSubmit={this.handleSubmit}>
      <div className="modal-body">

        <FormGroup label={gettext("New username")} for="id_username">
          <input type="text" id="id_username" className="form-control"
                 disabled={this.state.isLoading}
                 onChange={this.bindInput('username')}
                 value={this.state.username} />
        </FormGroup>

      </div>
      <div className="modal-footer">
        <button
          className="btn btn-default"
          data-dismiss="modal"
          disabled={this.state.isLoading}
          type="button"
        >
          {gettext("Cancel")}
        </button>
        <Button className="btn-primary" loading={this.state.isLoading}>
          {gettext("Change username")}
        </Button>
      </div>
    </form>;
    /* jshint ignore:end */
  }

  getModalBody() {
    if (this.state.error) {
      /* jshint ignore:start */
      return <ModalMessage icon="remove_circle_outline"
                           message={this.state.error} />;
      /* jshint ignore:end */
    } else if (this.state.isLoaded) {
      return this.getFormBody();
    } else {
      /* jshint ignore:start */
      return <Loader />;
      /* jshint ignore:end */
    }
  }

  getClassName() {
    if (this.state.error) {
      return "modal-dialog modal-message modal-rename-user";
    } else {
      return "modal-dialog modal-rename-user";
    }
  }

  render() {
    /* jshint ignore:start */
    return <div className={this.getClassName()}
                role="document">
      <div className="modal-content">
        <div className="modal-header">
          <button type="button" className="close" data-dismiss="modal"
                  aria-label={gettext("Close")}>
            <span aria-hidden="true">&times;</span>
          </button>
          <h4 className="modal-title">{gettext("Change username")}</h4>
        </div>
        {this.getModalBody()}
      </div>
    </div>;
    /* jshint ignore:end */
  }
}