import React from 'react';
import ajax from 'misago/services/ajax'; // jshint ignore:line
import snackbar from 'misago/services/snackbar'; // jshint ignore:line

export default class extends React.Component {
  /* jshint ignore:start */
  callApi = (op, successMessage) => {
    let errors = [];

    this.props.threads.forEach((thread) => {
      this.props.freezeThread(thread.id);

      ajax.patch(thread.api_url, [op]).then((data) => {
        this.props.freezeThread(thread.id);
        this.props.updateThread(data);
      }, (rejection) => {
        this.props.freezeThread(thread.id);
        errors.push(rejection);
      });
    });

    if (!errors.length) {
      snackbar.success(successMessage);
    }
  };

  pinGlobally = () => {
    this.callApi({
      op: 'replace',
      path: 'weight',
      value: 2
    }, gettext("Selected threads were pinned globally."));
  };

  pinLocally = () => {
    this.callApi({
      op: 'replace',
      path: 'weight',
      value: 1
    }, gettext("Selected threads were pinned locally."));
  };

  unpin = () => {
    this.callApi({
      op: 'replace',
      path: 'weight',
      value: 0
    }, gettext("Selected threads were unpinned."));
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
                className="btn btn-link">
          {gettext("Move threads")}
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
                className="btn btn-link">
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
                className="btn btn-link">
          {gettext("Close threads")}
        </button>
      </li>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getShowButton() {
    if (this.props.moderation.can_hide) {
      /* jshint ignore:start */
      return <li>
        <button type="button"
                className="btn btn-link">
          {gettext("Show threads")}
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
                className="btn btn-link">
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
                className="btn btn-link">
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
      {this.getOpenButton()}
      {this.getCloseButton()}
      {this.getShowButton()}
      {this.getHideButton()}
      {this.getDeleteButton()}
    </ul>;
    /* jshint ignore:end */
  }
}