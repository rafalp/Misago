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

    this.props.threads.forEach((thread) => {
      this.props.freezeThread(thread.id);

      ajax.patch(thread.api_url, ops).then((data) => {
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
      <MoveThreads callApi={this.callApi}
                   categories={this.props.categories}
                   categoriesMap={this.props.categoriesMap}
                   route={this.props.route}
                   user={this.props.user} />
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

    const errors = [];
    const countdown = new Countdown(() => {
      if (errors.length) {
        modal.show(<ErrorsModal errors={errors} />);
      } else {
        snackbar.success(gettext("Selected threads were deleted."));
      }

      // unfreeze non-deleted threads
      this.props.threads.forEach((thread) => {
        this.props.freezeThread(thread.id);
      });

      // reduce selection to non-deleted threads
      store.dispatch(select.all(this.props.threads.map(function(item) {
        return item.id;
      })));
    }, this.props.threads.length);

    this.props.threads.forEach((thread) => {
      this.props.freezeThread(thread.id);

      ajax.delete(thread.api_url).then((data) => {
        this.props.freezeThread(thread.id);
        this.props.deleteThread(thread);
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
  /* jshint ignore:end */

  getPinGloballyButton() {
    if (this.props.moderation.can_pin == 2) {
      /* jshint ignore:start */
      return <li>
        <button type="button"
                className="btn btn-link"
                onClick={this.pinGlobally}>
          {gettext("Pin threads globally")}
        </button>
      </li>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getPinLocallyButton() {
    if (this.props.moderation.can_pin > 0) {
      /* jshint ignore:start */
      return <li>
        <button type="button"
                className="btn btn-link"
                onClick={this.pinLocally}>
          {gettext("Pin threads locally")}
        </button>
      </li>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getUnpinButton() {
    if (this.props.moderation.can_pin > 0) {
      /* jshint ignore:start */
      return <li>
        <button type="button"
                className="btn btn-link"
                onClick={this.unpin}>
          {gettext("Unpin threads")}
        </button>
      </li>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getMoveButton() {
    if (this.props.moderation.can_move) {
      /* jshint ignore:start */
      return <li>
        <button type="button"
                className="btn btn-link"
                onClick={this.move}>
          {gettext("Move threads")}
        </button>
      </li>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getMergeButton() {
    if (this.props.moderation.can_merge) {
      /* jshint ignore:start */
      return <li>
        <button type="button"
                className="btn btn-link"
                onClick={this.merge}>
          {gettext("Merge threads")}
        </button>
      </li>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getApproveButton() {
    if (this.props.moderation.can_approve) {
      /* jshint ignore:start */
      return <li>
        <button type="button"
                className="btn btn-link"
                onClick={this.approve}>
          {gettext("Approve threads")}
        </button>
      </li>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getOpenButton() {
    if (this.props.moderation.can_close) {
      /* jshint ignore:start */
      return <li>
        <button type="button"
                className="btn btn-link"
                onClick={this.open}>
          {gettext("Open threads")}
        </button>
      </li>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getCloseButton() {
    if (this.props.moderation.can_close) {
      /* jshint ignore:start */
      return <li>
        <button type="button"
                className="btn btn-link"
                onClick={this.close}>
          {gettext("Close threads")}
        </button>
      </li>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getUnhideButton() {
    if (this.props.moderation.can_hide) {
      /* jshint ignore:start */
      return <li>
        <button type="button"
                className="btn btn-link"
                onClick={this.unhide}>
          {gettext("Unhide threads")}
        </button>
      </li>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getHideButton() {
    if (this.props.moderation.can_hide) {
      /* jshint ignore:start */
      return <li>
        <button type="button"
                className="btn btn-link"
                onClick={this.hide}>
          {gettext("Hide threads")}
        </button>
      </li>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getDeleteButton() {
    if (this.props.moderation.can_hide == 2) {
      /* jshint ignore:start */
      return <li>
        <button type="button"
                className="btn btn-link"
                onClick={this.delete}>
          {gettext("Delete threads")}
        </button>
      </li>;
      /* jshint ignore:end */
    } else {
      return null;
    }
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