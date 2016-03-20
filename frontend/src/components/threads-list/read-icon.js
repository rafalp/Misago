import React from 'react';

export default class extends React.Component {
  getClassName() {
    if (this.props.thread.is_read) {
      return 'read-status item-read';
    } else {
      return 'read-status item-new';
    }
  }

  getTitle() {
    if (this.props.thread.is_closed) {
      if (this.props.thread.is_read) {
        return gettext("This thread has no new posts. (closed)");
      } else {
        return gettext("This thread has new posts. (closed)");
      }
    } else {
      if (this.props.thread.is_read) {
        return gettext("This thread has no new posts.");
      } else {
        return gettext("This thread has new posts.");
      }
    }
  }

  getIcon() {
    if (this.props.thread.is_read) {
      return 'chat_bubble_outline';
    } else {
      return 'chat_bubble';
    }
  }

  render() {
    /* jshint ignore:start */
    return <div className={this.getClassName()} title={this.getTitle()}>
      <span className="material-icon">
        {this.getIcon()}
      </span>
    </div>;
    /* jshint ignore:end */
  }
}