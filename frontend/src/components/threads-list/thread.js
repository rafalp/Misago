import React from 'react';

export default class extends React.Component {
  render () {
    /* jshint ignore:start */
    return <li className="list-group-item">
      <div>
        <a href={this.props.thread.absolute_url} className="item-title thread-title">
          {this.props.thread.title}
        </a>
      </div>
    </li>;
    /* jshint ignore:end */
  }
}