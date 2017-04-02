import React from 'react';

export default class extends React.Component {
  getPinnedIcon() {
    if (this.props.thread.weight === 2) {
      /* jshint ignore:start */
      return <span className="thread-pinned-globally">
        <span className="material-icon">
          bookmark
        </span>
      </span>;
      /* jshint ignore:end */
    } else if (this.props.thread.weight === 1) {
      /* jshint ignore:start */
      return <span className="thread-pinned-locally">
        <span className="material-icon">
          bookmark_border
        </span>
      </span>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getUnapprovedIcon() {
    if (this.props.thread.is_unapproved) {
      /* jshint ignore:start */
      return <span className="thread-unapproved">
        <span className="material-icon">
          remove_circle
        </span>
      </span>;
      /* jshint ignore:end */
    } else if (this.props.thread.has_unapproved_posts) {
      /* jshint ignore:start */
      return <span className="thread-unapproved-posts">
        <span className="material-icon">
          remove_circle_outline
        </span>
      </span>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getHiddenIcon() {
    if (this.props.thread.is_hidden) {
      /* jshint ignore:start */
      return <span className="thread-hidden">
        <span className="material-icon">
          visibility_off
        </span>
      </span>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getClosedIcon() {
    if (this.props.thread.is_closed) {
      /* jshint ignore:start */
      return <span className="thread-closed">
        <span className="material-icon">
          lock_outline
        </span>
      </span>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  render () {
    /* jshint ignore:start */
    return <div className="thread-flags">
      {this.getPinnedIcon()}
      {this.getUnapprovedIcon()}
      {this.getHiddenIcon()}
      {this.getClosedIcon()}
    </div>;
    /* jshint ignore:end */
  }
}