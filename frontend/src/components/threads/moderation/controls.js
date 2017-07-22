import React from 'react';
import ErrorsModal from 'misago/components/threads/moderation/errors-list'; // jshint ignore:line
import MergeThreads from 'misago/components/threads/moderation/merge'; // jshint ignore:line
import MoveThreads from 'misago/components/threads/moderation/move'; // jshint ignore:line
import * as select from 'misago/reducers/selection'; // jshint ignore:line
import ajax from 'misago/services/ajax'; // jshint ignore:line
import modal from 'misago/services/modal'; // jshint ignore:line
import snackbar from 'misago/services/snackbar'; // jshint ignore:line
import store from 'misago/services/store'; // jshint ignore:line
import Countdown from 'misago/utils/countdown'; // jshint ignore:line

export default class extends React.Component {
  /* jshint ignore:start */
  callApi = (ops, successMessage, onSuccess=null) => {
    const errors = [];
    const countdown = new Countdown(() => {
      this.props.threads.forEach((thread) => {
        this.props.freezeThread(thread.id);
      });

      if (errors.length) {
        modal.show(<ErrorsModal errors={errors} />);
      } else {
        snackbar.success(successMessage);
        if (onSuccess) {
          onSuccess();
        }
      }
    }, this.props.threads.length);

    // update thread acl together with its state
    ops.push({op: 'add', path: 'acl', value: true});

    this.props.threads.forEach((thread) => {
      this.props.freezeThread(thread.id);

      ajax.patch(thread.api.index, ops).then((data) => {
        this.props.updateThread(data);
        countdown.count();
      }, (rejection) => {
        errors.push({
          thread: thread,
          errors: [rejection.detail]
        });

        countdown.count();
      });
    });
  };

  pinGlobally = () => {
    this.callApi([
      {
        op: 'replace',
        path: 'weight',
        value: 2
      }
    ], gettext("Selected threads were pinned globally."));
  };

  pinLocally = () => {
    this.callApi([
      {
        op: 'replace',
        path: 'weight',
        value: 1
      }
    ], gettext("Selected threads were pinned locally."));
  };

  unpin = () => {
    this.callApi([
      {
        op: 'replace',
        path: 'weight',
        value: 0
      }
    ], gettext("Selected threads were unpinned."));
  };

  approve = () => {
    this.callApi([
      {
        op: 'replace',
        path: 'is-unapproved',
        value: false
      }
    ], gettext("Selected threads were approved."));
  };

  open = () => {
    this.callApi([
      {
        op: 'replace',
        path: 'is-closed',
        value: false
      }
    ], gettext("Selected threads were opened."));
  };

  close = () => {
    this.callApi([
      {
        op: 'replace',
        path: 'is-closed',
        value: true
      }
    ], gettext("Selected threads were closed."));
  };

  unhide = () => {
    this.callApi([
      {
        op: 'replace',
        path: 'is-hidden',
        value: false
      }
    ], gettext("Selected threads were unhidden."));
  };

  hide = () => {
    this.callApi([
      {
        op: 'replace',
        path: 'is-hidden',
        value: true
      }
    ], gettext("Selected threads were hidden."));
  };

  move = () => {
    modal.show(
      <MoveThreads
        callApi={this.callApi}
        categories={this.props.categories}
        categoriesMap={this.props.categoriesMap}
        route={this.props.route}
        user={this.props.user}
      />
    );
  };

  merge = () => {
    const errors = [];
    this.props.threads.forEach((thread) => {
      if (!thread.acl.can_merge) {
        errors.append({
          'id': thread.id,
          'title': thread.title,
          'errors': [
            gettext("You don't have permission to merge this thread with others.")
          ]
        });
      }
    });

    if (this.props.threads.length < 2) {
      snackbar.info(
        gettext("You have to select at least two threads to merge."));
    } else if (errors.length) {
      modal.show(<ErrorsModal errors={errors} />);
      return;
    } else {
      modal.show(<MergeThreads {...this.props} />);
    }
  };

  delete = () => {
    if (!confirm(gettext("Are you sure you want to delete selected threads?"))) {
      return;
    }

    this.props.threads.map((thread) => {
      this.props.freezeThread(thread.id);
    });

    const ids = this.props.threads.map((thread) => { return thread.id; });

    ajax.delete(this.props.api, ids).then(() => {
      this.props.threads.map((thread) => {
        this.props.freezeThread(thread.id);
        this.props.deleteThread(thread);
      });

      snackbar.success(gettext("Selected threads were deleted."));
    }, (rejection) => {
      if (rejection.status === 400) {
        const failedThreads = rejection.map((thread) => { return thread.id; });

        this.props.threads.map((thread) => {
          this.props.freezeThread(thread.id);
          if (failedThreads.indexOf(thread.id) === -1) {
            this.props.deleteThread(thread);
          }
        });

        modal.show(<ErrorsModal errors={rejection} />);
      } else {
        snackbar.apiError(rejection);
      }
    });
  };
  /* jshint ignore:end */

  getPinGloballyButton() {
    if (this.props.moderation.can_pin !== 2) return null;

    /* jshint ignore:start */
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
          {gettext("Pin threads globally")}
        </button>
      </li>
    );
    /* jshint ignore:end */
  }

  getPinLocallyButton() {
    if (this.props.moderation.can_pin === 0) return null;

    /* jshint ignore:start */
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
          {gettext("Pin threads locally")}
        </button>
      </li>
    );
    /* jshint ignore:end */
  }

  getUnpinButton() {
    if (this.props.moderation.can_pin === 0) return null;

    /* jshint ignore:start */
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
          {gettext("Unpin threads")}
        </button>
      </li>
    );
    /* jshint ignore:end */
  }

  getMoveButton() {
    if (!this.props.moderation.can_move) return null;

    /* jshint ignore:start */
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
          {gettext("Move threads")}
        </button>
      </li>
    );
    /* jshint ignore:end */
  }

  getMergeButton() {
    if (!this.props.moderation.can_merge) return null;

    /* jshint ignore:start */
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
          {gettext("Merge threads")}
        </button>
      </li>
    );
    /* jshint ignore:end */
  }

  getApproveButton() {
    if (!this.props.moderation.can_approve) return null;

    /* jshint ignore:start */
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
          {gettext("Approve threads")}
        </button>
      </li>
    );
    /* jshint ignore:end */
  }

  getOpenButton() {
    if (!this.props.moderation.can_close) return null;

    /* jshint ignore:start */
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
          {gettext("Open threads")}
        </button>
      </li>
    );
    /* jshint ignore:end */
  }

  getCloseButton() {
    if (!this.props.moderation.can_close) return null;

    /* jshint ignore:start */
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
          {gettext("Close threads")}
        </button>
      </li>
    );
    /* jshint ignore:end */
  }

  getUnhideButton() {
    if (!this.props.moderation.can_unhide) return null;

    /* jshint ignore:start */
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
          {gettext("Unhide threads")}
        </button>
      </li>
    );
    /* jshint ignore:end */
  }

  getHideButton() {
    if (!this.props.moderation.can_hide) return null;

    /* jshint ignore:start */
    return (
      <li>
        <button
          onClick={this.hide}
          type="button"
          className="btn btn-link"
        >
          <span className="material-icon">
            visibility_off
          </span>
          {gettext("Hide threads")}
        </button>
      </li>
    );
    /* jshint ignore:end */
  }

  getDeleteButton() {
    if (!this.props.moderation.can_delete) return null;

    /* jshint ignore:start */
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
          {gettext("Delete threads")}
        </button>
      </li>
    );
    /* jshint ignore:end */
  }

  render() {
    /* jshint ignore:start */
    return <ul className={this.props.className}>
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
    </ul>;
    /* jshint ignore:end */
  }
}