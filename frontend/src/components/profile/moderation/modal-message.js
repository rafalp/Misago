import React from 'react';

export default class extends React.Component {
  render() {
    /* jshint ignore:start */
    return <div className="modal-body">
      <div className="message-icon">
        <span className="material-icon">
          {this.props.icon || 'remove_circle_outline'}
        </span>
      </div>
      <div className="message-body">
        <p className="lead">
          {this.props.message}
        </p>
      </div>
    </div>;
    /* jshint ignore:end */
  }
}