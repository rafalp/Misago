import React from 'react'; // jshint ignore:line
import Button from 'misago/components/button'; // jshint ignore:line
import Form from 'misago/components/form';
import FormGroup from 'misago/components/form-group'; // jshint ignore:line
import Loader from 'misago/components/modal-loader'; // jshint ignore:line
import YesNoSwitch from 'misago/components/yes-no-switch'; // jshint ignore:line
import ModalMessage from 'misago/components/modal-message'; // jshint ignore:line
import { updateAvatar } from 'misago/reducers/users'; // jshint ignore:line
import ajax from 'misago/services/ajax';
import snackbar from 'misago/services/snackbar';
import store from 'misago/services/store';

export default class extends Form {
  constructor(props) {
    super(props);

    this.state = {
      isLoaded: false,
      isLoading: false,
      error: null,

      is_avatar_locked: '',
      avatar_lock_user_message: '',
      avatar_lock_staff_message: ''
    };
  }

  componentDidMount() {
    ajax.get(this.props.profile.api_url.moderate_avatar).then((options) => {
      this.setState({
        isLoaded: true,

        is_avatar_locked: options.is_avatar_locked,
        avatar_lock_user_message: options.avatar_lock_user_message,
        avatar_lock_staff_message: options.avatar_lock_staff_message
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
    return ajax.post(this.props.profile.api_url.moderate_avatar, {
      is_avatar_locked: this.state.is_avatar_locked,
      avatar_lock_user_message: this.state.avatar_lock_user_message,
      avatar_lock_staff_message: this.state.avatar_lock_staff_message
    });
  }

  handleSuccess(apiResponse) {
    store.dispatch(updateAvatar(this.props.profile, apiResponse.avatar_hash));
    snackbar.success(gettext("Avatar controls have been changed."));
  }

  getFormBody() {
    /* jshint ignore:start */
    return <form onSubmit={this.handleSubmit}>
      <div className="modal-body">

        <FormGroup label={gettext("Lock avatar")}
                   helpText={gettext("Locking user avatar will prohibit user from changing his avatar and will reset his/her avatar to default one.")}
                   for="id_is_avatar_locked">
          <YesNoSwitch id="id_is_avatar_locked"
                       disabled={this.state.isLoading}
                       iconOn="lock_outline"
                       iconOff="lock_open"
                       labelOn={gettext("Disallow user from changing avatar")}
                       labelOff={gettext("Allow user to change avatar")}
                       onChange={this.bindInput('is_avatar_locked')}
                       value={this.state.is_avatar_locked} />
        </FormGroup>

        <FormGroup label={gettext("User message")}
                   helpText={gettext("Optional message for user explaining why he/she is prohibited form changing avatar.")}
                   for="id_avatar_lock_user_message">
          <textarea id="id_avatar_lock_user_message"
                    className="form-control"
                    rows="4"
                    disabled={this.state.isLoading}
                    onChange={this.bindInput('avatar_lock_user_message')}
                    value={this.state.avatar_lock_user_message} />
        </FormGroup>

        <FormGroup label={gettext("Staff message")}
                   helpText={gettext("Optional message for forum team members explaining why user is prohibited form changing avatar.")}
                   for="id_avatar_lock_staff_message">
          <textarea id="id_avatar_lock_staff_message"
                    className="form-control"
                    rows="4"
                    disabled={this.state.isLoading}
                    onChange={this.bindInput('avatar_lock_staff_message')}
                    value={this.state.avatar_lock_staff_message} />
        </FormGroup>

      </div>
      <div className="modal-footer">
        <button type="button" className="btn btn-default" data-dismiss="modal">
          {gettext("Close")}
        </button>
        <Button className="btn-primary" loading={this.state.isLoading}>
          {gettext("Save changes")}
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
      return "modal-dialog modal-message modal-avatar-controls";
    } else {
      return "modal-dialog modal-avatar-controls";
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
          <h4 className="modal-title">{gettext("Avatar controls")}</h4>
        </div>
        {this.getModalBody()}
      </div>
    </div>;
    /* jshint ignore:end */
  }
}