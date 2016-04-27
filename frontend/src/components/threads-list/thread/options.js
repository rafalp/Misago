import React from 'react';
import SubscriptionCompact from 'misago/components/threads-list/thread/subscription/compact'; // jshint ignore:line
import SubscriptionFull from 'misago/components/threads-list/thread/subscription/full'; // jshint ignore:line
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
          <span className="icon-legend">
            {this.props.isSelected
              ? gettext("Selected")
              : gettext("Select")}
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
    return <div className="thread-options">
      <ul className="list-inline">
        {this.getSelectToggle()}
        <SubscriptionFull thread={this.props.thread} />
        <SubscriptionCompact thread={this.props.thread} />
      </ul>
    </div>;
    /* jshint ignore:end */
  }
}