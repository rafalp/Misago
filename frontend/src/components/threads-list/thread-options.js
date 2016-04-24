import React from 'react';
import SubscriptionToggle from 'misago/components/threads-list/subscription-toggle'; // jshint ignore:line
import * as select from 'misago/reducers/selection'; // jshint ignore:line
import store from 'misago/services/store'; // jshint ignore:line

export default class extends React.Component {
  /* jshint ignore:start */
  toggleSelection = () => {
    store.dispatch(select.item(this.props.thread.id));
  };
  /* jshint ignore:end */

  getSelectToggle() {
    if (this.props.thread.moderation.length) {
      /* jshint ignore:start */
      return <li>
        <button className="btn btn-default btn-checkbox"
                onClick={this.toggleSelection}>
          <span className="material-icon">
            {this.props.isSelected
              ? 'check_box'
              : 'check_box_outline_blank'}
          </span>
        </button>
      </li>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  render() {
    /* jshint ignore:start */
    return <ul className="list-inline thread-options">
      <SubscriptionToggle thread={this.props.thread} />
      {this.getSelectToggle()}
    </ul>
    /* jshint ignore:end */
  }
}