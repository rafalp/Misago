import React from 'react';

export default class extends React.Component {
  render() {
    /* jshint ignore:start */
    return <div className={this.props.className || "loader"}>
      <div className="loader-spinning-wheel"></div>
    </div>;
    /* jshint ignore:end */
  }
}
