import React from 'react';

export default class extends React.Component {
  render () {
    /* jshint ignore:start */
    return <li className="list-group-item">
      {this.props.thread.title}
    </li>;
    /* jshint ignore:end */
  }
}