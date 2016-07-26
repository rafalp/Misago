import React from 'react';
import Header from 'misago/components/thread/header'; // jshint ignore:line

export default class extends React.Component {
  render() {
    /* jshint ignore:start */
    return <div className="page page-thread">
      <Header thread={this.props.thread} />
      <div className="container">
        Thread content here
      </div>
    </div>;
    /* jshint ignore:end */
  }
}