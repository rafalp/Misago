import React from 'react';
import SubscriptionToggle from 'misago/components/threads-list/subscription-toggle'; // jshint ignore:line

export default class extends React.Component {
  /* jshint ignore:start */
  toggleSelection = () => {
    this.props.selectThread(this.props.thread.id);
  };
  /* jshint ignore:end */

  getEditToggle() {
    if (this.props.thread.acl.can_edit || this.props.thread.acl.can_move) {
      /* jshint ignore:start */
      return <li>
        <button className="btn btn-default btn-edit">
          <span className="material-icon">
            edit
          </span>
        </button>
      </li>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getSelectToggle() {
    if (this.props.thread.moderation.length) {
      /* jshint ignore:start */
      return <li>
        <button className="btn btn-default btn-select"
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
      {this.getEditToggle()}
      {this.getSelectToggle()}
    </ul>
    /* jshint ignore:end */
  }
}