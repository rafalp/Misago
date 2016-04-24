import React from 'react';

export default class extends React.Component {
  render() {
    /* jshint ignore:start */
    return <ul className={this.props.className}>
      <li>
        <button className="btn btn-link"
                type="button"
                onClick={this.props.selectAll}>
          <span className="material-icon">check_box</span>
          {gettext("Select all")}
        </button>
      </li>
      <li>
        <button className="btn btn-link"
                type="button"
                onClick={this.props.selectNone}>
          <span className="material-icon">check_box_outline_blank</span>
          {gettext("Select none")}
        </button>
      </li>
    </ul>;
    /* jshint ignore:end */
  }
}