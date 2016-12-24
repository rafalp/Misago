/* jshint ignore:start */
import React from 'react';
import Form from './form';
import FormGroup from 'misago/components/form-group';
import * as participants from 'misago/reducers/participants';
import { updateAcl } from 'misago/reducers/thread';
import ajax from 'misago/services/ajax';
import modal from 'misago/services/modal';
import snackbar from 'misago/services/snackbar';
import store from 'misago/services/store';

export default class extends Form {
  constructor(props) {
    super(props);

    this.state = {
      isLoading: false,

      username: ''
    };
  }

  onUsernameChange = (event) => {
    this.changeValue('username', event.target.value);
  };

  clean() {
    if (!this.state.username.trim().length) {
      snackbar.error(gettext("You have to enter user name."));
      return false;
    }

    return true;
  }

  send() {
    return ajax.patch(this.props.thread.api.index, [
      {op: 'add', path: 'participants', value: this.state.username},
      {op: 'add', path: 'acl', value: 1}
    ]);
  }

  handleSuccess(data) {
    store.dispatch(updateAcl(data));
    store.dispatch(participants.replace(data.participants));

    snackbar.success(gettext("New participant has been added to thread."));

    modal.hide();
  }

  render() {
    return (
      <div className="modal-dialog modal-sm" role="document">
        <form onSubmit={this.handleSubmit}>
          <div className="modal-content">
            <ModalHeader />
            <div className="modal-body">
              <FormGroup for="id_username" label={gettext("User to add")}>
                <input
                  id="id_username"
                  className="form-control"
                  disabled={this.state.isLoading}
                  onChange={this.onUsernameChange}
                  type="text"
                  value={this.state.title}
                />
              </FormGroup>
            </div>
            <div className="modal-footer">
              <button className="btn btn-block btn-primary" disabled={this.state.isLoading}>
                {gettext("Add participant")}
              </button>
            </div>
          </div>
        </form>
      </div>
    );
  }
}

export function ModalHeader(props) {
  return (
    <div className="modal-header">
      <button
        aria-label={gettext("Close")}
        className="close"
        data-dismiss="modal"
        type="button"
      >
        <span aria-hidden="true">&times;</span>
      </button>
      <h4 className="modal-title">{gettext("Add participant")}</h4>
    </div>
  );
}
