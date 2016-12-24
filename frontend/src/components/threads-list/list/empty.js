import React from 'react';
import DiffMessage from 'misago/components/threads-list/list/diff-message'; // jshint ignore:line

export default class extends React.Component {
  getDiffMessage() {
    if (this.props.diffSize === 0) return null;

    /* jshint ignore:start */
    return (
      <DiffMessage
        applyDiff={this.props.applyDiff}
        diffSize={this.props.diffSize}
      />
    );
    /* jshint ignore:end */
  }

  render () {
    /* jshint ignore:start */
    return (
      <div className="threads-list ui-ready">
        <ul className="list-group">
          {this.getDiffMessage()}
          {this.props.children}
        </ul>
      </div>
    );
    /* jshint ignore:end */
  }
}