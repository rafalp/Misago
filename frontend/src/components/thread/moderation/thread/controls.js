// jshint ignore:start
import React from 'react';
import MergeModal from './merge'; // jshint ignore:line
import MoveModal from './move'; // jshint ignore:line
import * as thread from 'misago/reducers/thread';
import ajax from 'misago/services/ajax'; // jshint ignore:line
import modal from 'misago/services/modal'; // jshint ignore:line
import snackbar from 'misago/services/snackbar'; // jshint ignore:line
import store from 'misago/services/store'; // jshint ignore:line

export default class extends React.Component {
  callApi = (ops, successMessage) => {
    store.dispatch(thread.busy());

    // by the chance update thread acl too
    ops.push({op: 'add', path: 'acl', value: true});

    ajax.patch(this.props.thread.api.index, ops).then((data) => {
      store.dispatch(thread.update(data));
      store.dispatch(thread.release());
      snackbar.success(successMessage);
    }, (rejection) => {
      store.dispatch(thread.release());
      if (rejection.status === 400) {
        snackbar.error(rejection.detail[0]);
      } else {
        snackbar.apiError(rejection);
      }
    });
  };

  pinGlobally = () => {
    this.callApi([
      {
        op: 'replace',
        path: 'weight',
        value: 2
      }
    ], gettext("Thread has been pinned globally."));
  };

  pinLocally = () => {
    this.callApi([
      {
        op: 'replace',
        path: 'weight',
        value: 1
      }
    ], gettext("Thread has been pinned locally."));
  };

  unpin = () => {
    this.callApi([
      {
        op: 'replace',
        path: 'weight',
        value: 0
      }
    ], gettext("Thread has been unpinned."));
  };

  approve = () => {
    this.callApi([
      {
        op: 'replace',
        path: 'is-unapproved',
        value: false
      }
    ], gettext("Thread has been approved."));
  };

  open = () => {
    this.callApi([
      {
        op: 'replace',
        path: 'is-closed',
        value: false
      }
    ], gettext("Thread has been opened."));
  };

  close = () => {
    this.callApi([
      {
        op: 'replace',
        path: 'is-closed',
        value: true
      }
    ], gettext("Thread has been closed."));
  };

  unhide = () => {
    this.callApi([
      {
        op: 'replace',
        path: 'is-hidden',
        value: false
      }
    ], gettext("Thread has been made visible."));
  };

  hide = () => {
    this.callApi([
      {
        op: 'replace',
        path: 'is-hidden',
        value: true
      }
    ], gettext("Thread has been made hidden."));
  };

  move = () => {
    modal.show(
      <MoveModal
        posts={this.props.posts}
        thread={this.props.thread}
      />
    );
  };

  merge = () => {
    modal.show(
      <MergeModal thread={this.props.thread} />
    );
  };

  delete = () => {
    if (!confirm(gettext("Are you sure you want to delete this thread?"))) {
      return;
    }

    store.dispatch(thread.busy());

    ajax.delete(this.props.thread.api.index).then((data) => {
      snackbar.success(gettext("Thread has been deleted."))
      window.location = this.props.thread.category.absolute_url;
    }, (rejection) => {
      store.dispatch(thread.release());
      snackbar.apiError(rejection);
    });
  };

  getPinGloballyButton() {
    if (this.props.thread.weight < 2 && this.props.thread.acl.can_pin == 2) {
      return (
        <li>
          <button type="button"
                  className="btn btn-link"
                  onClick={this.pinGlobally}>
            {gettext("Pin globally")}
          </button>
        </li>
      );
    } else {
      return null;
    }
  }

  getPinLocallyButton() {
    if (this.props.thread.weight !== 1 && this.props.thread.acl.can_pin > 0) {
      return (
        <li>
          <button type="button"
                  className="btn btn-link"
                  onClick={this.pinLocally}>
            {gettext("Pin locally")}
          </button>
        </li>
      );
    } else {
      return null;
    }
  }

  getUnpinButton() {
    if (this.props.thread.weight > 0 && this.props.thread.acl.can_pin > 0) {
      return (
        <li>
          <button type="button"
                  className="btn btn-link"
                  onClick={this.unpin}>
            {gettext("Unpin")}
          </button>
        </li>
      );
    } else {
      return null;
    }
  }

  getMoveButton() {
    if (this.props.thread.acl.can_move) {
      return (
        <li>
          <button type="button"
                  className="btn btn-link"
                  onClick={this.move}>
            {gettext("Move")}
          </button>
        </li>
      );
    } else {
      return null;
    }
  }

  getMergeButton() {
    if (this.props.thread.acl.can_merge) {
      return (
        <li>
          <button type="button"
                  className="btn btn-link"
                  onClick={this.merge}>
            {gettext("Merge")}
          </button>
        </li>
      );
    } else {
      return null;
    }
  }

  getApproveButton() {
    if (this.props.thread.is_unapproved && this.props.thread.acl.can_approve) {
      return (
        <li>
          <button type="button"
                  className="btn btn-link"
                  onClick={this.approve}>
            {gettext("Approve")}
          </button>
        </li>
      );
    } else {
      return null;
    }
  }

  getOpenButton() {
    if (this.props.thread.is_closed && this.props.thread.acl.can_close) {
      return (
        <li>
          <button type="button"
                  className="btn btn-link"
                  onClick={this.open}>
            {gettext("Open")}
          </button>
        </li>
      );
    } else {
      return null;
    }
  }

  getCloseButton() {
    if (!this.props.thread.is_closed && this.props.thread.acl.can_close) {
      return (
        <li>
          <button type="button"
                  className="btn btn-link"
                  onClick={this.close}>
            {gettext("Close")}
          </button>
        </li>
      );
    } else {
      return null;
    }
  }

  getUnhideButton() {
    if (this.props.thread.is_hidden && this.props.thread.acl.can_hide) {
      return (
        <li>
          <button type="button"
                  className="btn btn-link"
                  onClick={this.unhide}>
            {gettext("Unhide")}
          </button>
        </li>
      );
    } else {
      return null;
    }
  }

  getHideButton() {
    if (!this.props.thread.is_hidden && this.props.thread.acl.can_hide) {
      return (
        <li>
          <button type="button"
                  className="btn btn-link"
                  onClick={this.hide}>
            {gettext("Hide")}
          </button>
        </li>
      );
    } else {
      return null;
    }
  }

  getDeleteButton() {
    if (this.props.thread.acl.can_hide == 2) {
      return (
        <li>
          <button type="button"
                  className="btn btn-link"
                  onClick={this.delete}>
            {gettext("Delete")}
          </button>
        </li>
      );
    } else {
      return null;
    }
  }

  render() {
    return (
      <ul className="dropdown-menu dropdown-menu-right stick-to-bottom">
        {this.getPinGloballyButton()}
        {this.getPinLocallyButton()}
        {this.getUnpinButton()}
        {this.getMoveButton()}
        {this.getMergeButton()}
        {this.getApproveButton()}
        {this.getOpenButton()}
        {this.getCloseButton()}
        {this.getUnhideButton()}
        {this.getHideButton()}
        {this.getDeleteButton()}
      </ul>
    );
  }
}