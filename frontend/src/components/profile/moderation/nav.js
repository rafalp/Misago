import React from 'react';

export default class extends React.Component {
  render() {
    // jshint ignore:start
    return <ul className="dropdown-menu dropdown-menu-right" role="menu">
      <li>
        <button className="btn-link">
          <span className="material-icon">
            explore
          </span>
          Moderate somehow
        </button>
      </li>
      <li>
        <button className="btn-link">
          <span className="material-icon">
            explore
          </span>
          Moderate else
        </button>
      </li>
    </ul>;
    // jshint ignore:end
  }
}