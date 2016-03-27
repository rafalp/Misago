import React from 'react';

export default class extends React.Component {
  getEmptyMessage() {
    if (this.props.emptyMessage) {
      return this.props.emptyMessage;
    } else {
      return gettext("No name changes have been recorded for your account.");
    }
  }

  render() {
    /* jshint ignore:start */
    return <div className="username-history ui-ready">
      <ul className="list-group">
        <li className="list-group-item empty-message">
          {this.getEmptyMessage()}
        </li>
      </ul>
    </div>;
    /* jshint ignore:end */
  }
}