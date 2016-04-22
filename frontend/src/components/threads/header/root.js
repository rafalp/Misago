import React from 'react';

export default class extends React.Component {
  getClassName() {
    if (this.props.route.lists.length > 1) {
      return 'page-header tabbed';
    } else {
      return 'page-header';
    }
  }

  render() {
    /* jshint ignore:start */
    return <div className={this.getClassName()}>
      <div className="container">
        <h1 className="pull-left">{this.props.title}</h1>
      </div>
    </div>;
    /* jshint ignore:end */
  }
}