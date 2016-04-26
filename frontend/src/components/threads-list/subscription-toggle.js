import React from 'react';
import Button from 'misago/components/button'; // jshint ignore:line
import { patch } from 'misago/reducers/threads'; // jshint ignore:line
import ajax from 'misago/services/ajax'; // jshint ignore:line
import snackbar from 'misago/services/snackbar'; // jshint ignore:line
import store from 'misago/services/store'; // jshint ignore:line

/* jshint ignore:start */
const STATE_UPDATES = {
  'unsubscribe': null,
  'notify': false,
  'email': true
};
/* jshint ignore:end */

export default class extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      isLoading: false
    };
  }

  /* jshint ignore:start */
  setSubscription = (newState) => {
    this.setState({
      isLoading: true
    });

    let oldState = this.props.thread.subscription;

    store.dispatch(patch(this.props.thread, {
      subscription: STATE_UPDATES[newState]
    }));

    ajax.patch(this.props.thread.api_url, [
      {op: 'replace', path: 'subscription', value: newState}
    ]).then(() => {
      this.setState({
        isLoading: false
      });
    }, (rejection) => {
      this.setState({
        isLoading: false
      });
      store.dispatch(patch(this.props.thread, {
        subscription: STATE_UPDATES[oldState]
      }));
      snackbar.apiError(rejection);
    });
  };

  unsubscribe = () => {
    this.setSubscription('unsubscribe');
  };

  notify = () => {
    this.setSubscription('notify');
  };

  email = () => {
    this.setSubscription('email');
  };
  /* jshint ignore:end */

  getIcon() {
    if (this.props.thread.subscription === true) {
      return 'star';
    } else if (this.props.thread.subscription === false) {
      return 'star_half';
    } else {
      return 'star_border';
    }
  }

  getLegend() {
    if (this.props.thread.subscription === true) {
      return 'Email';
    } else if (this.props.thread.subscription === false) {
      return gettext("Enabled");
    } else {
      return gettext("Disabled");
    }
  }

  getClassName() {
    if (this.props.thread.subscription === true) {
      return "btn btn-default btn-subscribe btn-subscribe-full dropdown-toggle";
    } else if (this.props.thread.subscription === false) {
      return "btn btn-default btn-subscribe btn-subscribe-half dropdown-toggle";
    } else {
      return "btn btn-default btn-subscribe dropdown-toggle";
    }
  }

  render() {
    /* jshint ignore:start */
    return <li>
      <div className="btn-group">
        <button type="button"
                className={this.getClassName()}
                data-toggle="dropdown"
                aria-haspopup="true"
                aria-expanded="false"
                disabled={this.state.isBusy}>
          <span className="material-icon">
            {this.getIcon()}
          </span>
          <span className="icon-legend">
            {this.getLegend()}
          </span>
        </button>
        <ul className="dropdown-menu dropdown-menu-right">
          <li>
            <button className="btn-link" onClick={this.unsubscribe}>
              <span className="material-icon">
                star_border
              </span>
              {gettext("Unsubscribe")}
            </button>
          </li>
          <li>
            <button className="btn-link" onClick={this.notify}>
              <span className="material-icon">
                star_half
              </span>
              {gettext("Subscribe")}
            </button>
          </li>
          <li>
            <button className="btn-link" onClick={this.email}>
              <span className="material-icon">
                star
              </span>
              {gettext("Subscribe with e-mail")}
            </button>
          </li>
        </ul>
      </div>
    </li>;
    /* jshint ignore:end */
  }
}