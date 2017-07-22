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
      window.location = this.props.thread.category.url.index;
    }, (rejection) => {
      store.dispatch(thread.release());
      snackbar.apiError(rejection);
    });
  };

  getPinGloballyButton() {
    if (this.props.thread.weight === 2) return null;
    if (this.props.thread.acl.can_pin !== 2) return null;

    return (
      <li>
        <button
          className="btn btn-link"
          onClick={this.pinGlobally}
          type="button"
        >
          <span className="material-icon">
            bookmark
          </span>
          {gettext("Pin globally")}
        </button>
      </li>
    );
  }

  getPinLocallyButton() {
    if (this.props.thread.weight === 1) return null;
    if (this.props.thread.acl.can_pin === 0) return null;

    return (
      <li>
        <button
          className="btn btn-link"
          onClick={this.pinLocally}
          type="button"
        >
          <span className="material-icon">
            bookmark_border
          </span>
          {gettext("Pin locally")}
        </button>
      </li>
    );
  }

  getUnpinButton() {
    if (this.props.thread.weight === 0) return null;
    if (this.props.thread.acl.can_pin === 0) return null;

    return (
      <li>
        <button
          className="btn btn-link"
          onClick={this.unpin}
          type="button"
        >
          <span className="material-icon">
            panorama_fish_eye
          </span>
          {gettext("Unpin")}
        </button>
      </li>
    );
  }

  getMoveButton() {
    if (!this.props.thread.acl.can_move) return null;

    return (
      <li>
        <button
          className="btn btn-link"
          onClick={this.move}
          type="button"
        >
          <span className="material-icon">
            arrow_forward
          </span>
          {gettext("Move")}
        </button>
      </li>
    );
  }

  getMergeButton() {
    if (!this.props.thread.acl.can_merge) return null;

    return (
      <li>
        <button
          className="btn btn-link"
          onClick={this.merge}
          type="button"
        >
          <span className="material-icon">
            call_merge
          </span>
          {gettext("Merge")}
        </button>
      </li>
    );
  }

  getApproveButton() {
    if (!this.props.thread.is_unapproved) return null;
    if (!this.props.thread.acl.can_approve) return null;

    return (
      <li>
        <button
          className="btn btn-link"
          onClick={this.approve}
          type="button"
        >
          <span className="material-icon">
            done
          </span>
          {gettext("Approve")}
        </button>
      </li>
    );
  }

  getOpenButton() {
    if (!this.props.thread.is_closed) return null;
    if (!this.props.thread.acl.can_close) return null;

    return (
      <li>
        <button
          className="btn btn-link"
          onClick={this.open}
          type="button"
        >
          <span className="material-icon">
            lock_open
          </span>
          {gettext("Open")}
        </button>
      </li>
    );
  }

  getCloseButton() {
    if (this.props.thread.is_closed) return null;
    if (!this.props.thread.acl.can_close) return null;

    return (
      <li>
        <button
          className="btn btn-link"
          onClick={this.close}
          type="button"
        >
          <span className="material-icon">
            lock_outline
          </span>
          {gettext("Close")}
        </button>
      </li>
    );
  }

  getUnhideButton() {
    if (!this.props.thread.is_hidden) return null;
    if (!this.props.thread.acl.can_unhide) return null;

    return (
      <li>
        <button
          className="btn btn-link"
          onClick={this.unhide}
          type="button"
        >
          <span className="material-icon">
            visibility
          </span>
          {gettext("Unhide")}
        </button>
      </li>
    );
  }

  getHideButton() {
    if (this.props.thread.is_hidden) return null;
    if (!this.props.thread.acl.can_hide) return null;

    return (
      <li>
        <button
          className="btn btn-link"
          onClick={this.hide}
          type="button"
        >
          <span className="material-icon">
            visibility_off
          </span>
          {gettext("Hide")}
        </button>
      </li>
    );
  }

  getDeleteButton() {
    if (!this.props.thread.acl.can_delete) return null;

    return (
      <li>
        <button
          className="btn btn-link"
          onClick={this.delete}
          type="button"
        >
          <span className="material-icon">
            clear
          </span>
          {gettext("Delete")}
        </button>
      </li>
    );
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