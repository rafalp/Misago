import React from 'react';

export default class Loader extends React.Component {
  render() {
    /* jshint ignore:start */
    return <div className="loader-compact">
      <div className="bounce1"></div>
      <div className="bounce2"></div>
      <div className="bounce3"></div>
    </div>;
    /* jshint ignore:end */
  }
}
