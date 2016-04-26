import React from 'react';
import DiffMessage from 'misago/components/threads-list/list/diff-message'; // jshint ignore:line

export default class extends React.Component {
  getDiffMessage() {
    if (this.props.diffSize > 0) {
      /* jshint ignore:start */
      return <DiffMessage diffSize={this.props.diffSize}
                          applyDiff={this.props.applyDiff} />;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  render () {
    /* jshint ignore:start */
    return <div className="threads-list ui-ready">
      <ul className="list-group">
        {this.getDiffMessage()}
        {this.props.children}
      </ul>
    </div>;
    /* jshint ignore:end */
  }
}