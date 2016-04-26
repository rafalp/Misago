import React from 'react';
import Category from 'misago/components/threads-list/thread/category'; // jshint ignore:line

export default class extends React.Component {
  getPath() {
    let top = this.props.categories[this.props.thread.top_category];
    let bottom = this.props.categories[this.props.thread.category];

    if (top && bottom && top.id !== bottom.id) {
      /* jshint ignore:start */
      return <li className="thread-path">
        <Category category={bottom} list={this.props.list} />
      </li>;
      /* jshint ignore:end */
    } else if (top) {
      /* jshint ignore:start */
      return <li className="thread-path">
        <Category category={top} list={this.props.list} />
      </li>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getRepliesCount() {
    /* jshint ignore:start */
    return <li className="thread-replies-count">
      <span className="material-icon">
        forum
      </span>
      <span className="icon-legend">
        {this.props.thread.replies}
      </span>
    </li>;
    /* jshint ignore:end */
  }

  getLastReply() {
    /* jshint ignore:start */
    return <li className="thread-last-reply-clock">
      <span className="material-icon">
        schedule
      </span>
      <span className="icon-legend">
        {this.props.thread.last_post_on.fromNow()}
      </span>
    </li>;
    /* jshint ignore:end */
  }

  render () {
    /* jshint ignore:start */
    return <ul className="thread-details-compact list-inline">
      {this.getPath()}
      {this.getRepliesCount()}
      {this.getLastReply()}
    </ul>;
    /* jshint ignore:end */
  }
}