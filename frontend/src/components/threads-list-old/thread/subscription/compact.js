import React from 'react'; // jshint ignore:line
import SubscriptionFull from 'misago/components/threads-list/thread/subscription/full'; // jshint ignore:line
import OptionsModal from 'misago/components/threads-list/thread/subscription/modal'; // jshint ignore:line
import modal from 'misago/services/modal'; // jshint ignore:line

export default class extends SubscriptionFull {
  /* jshint ignore:start */
  showOptions = () => {
    modal.show(<OptionsModal thread={this.props.thread} />);
  };
  /* jshint ignore:end */

  render() {
    /* jshint ignore:start */
    return <li className="hidden-md hidden-lg">
      <button type="button"
              className={this.getClassName()}
              disabled={this.props.disabled}
              onClick={this.showOptions}>
        <span className="material-icon">
          {this.getIcon()}
        </span>
        <span className="icon-legend">
          {this.getLegend()}
        </span>
      </button>
    </li>;
    /* jshint ignore:end */
  }
}