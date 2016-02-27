import React from 'react';

export default class extends React.Component {
  render() {
    /* jshint ignore:start */
    return <div className="message-panel">

      <div className="message-icon">
        <span className="material-icon">info_outline</span>
      </div>

      <div className="message-body">
        <p className="lead">{gettext("No categories are available.")}</p>
        <p>{gettext("No categories are currently defined or you don't have permission to see them.")}</p>
      </div>

    </div>;
    /* jshint ignore:end */
  }
}