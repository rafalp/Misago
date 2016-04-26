import React from 'react';

export default class extends React.Component {
  getClassName() {
    if (this.props.hiddenOnMobile) {
      return 'list-group-item hidden-xs hidden-sm';
    } else {
      return 'list-group-item';
    }
  }

  render () {
    /* jshint ignore:start */
    return <li className={this.getClassName()}>
      Loading...
    </li>;
    /* jshint ignore:end */
  }
}