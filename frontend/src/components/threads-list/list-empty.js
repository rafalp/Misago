import React from 'react';

export default class extends React.Component {
  render () {
    /* jshint ignore:start */
    return <div className="threads-list ui-ready">
      <ul className="list-group">
        {this.props.children}
      </ul>
    </div>;
    /* jshint ignore:end */
  }
}