import React from 'react';
import Breadcrumbs from './breadcrumbs'; // jshint ignore:line
import Stats from './stats'; // jshint ignore:line

export default class extends React.Component {
  render() {
    /* jshint ignore:start */
    return <div className="page-header with-stats with-breadcrumbs">
      <Breadcrumbs path={this.props.thread.path} />
      <div className="container">
        <h1>{this.props.thread.title}</h1>
      </div>
      <Stats thread={this.props.thread} />
    </div>;
    /* jshint ignore:end */
  }
}