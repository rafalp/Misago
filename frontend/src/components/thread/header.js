import React from 'react';

export default class extends React.Component {
  render() {
    /* jshint ignore:start */
    return <div className="page-header with-stats with-breadcrumbs">
      <div className="container">
        <h1>{this.props.thread.title}</h1>
      </div>
    </div>;
    /* jshint ignore:end */
  }
}