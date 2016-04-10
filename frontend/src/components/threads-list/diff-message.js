import React from 'react';

export default class extends React.Component {
  getMessage() {
    let label = ngettext(
      "There is %(threads)s new or updated thread. Click to see it.",
      "There are %(threads)s new or updated threads. Click to see them.",
      this.props.diffSize);

    return interpolate(label, {
      threads: this.props.diffSize
    }, true);
  }

  render () {
    /* jshint ignore:start */
    return <li className="list-group-item diff-message">
      <button type="button"
              className="btn btn-link"
              onClick={this.props.applyDiff}>
        <span className="material-icon">
          cached
        </span>
        {this.getMessage()}
      </button>
    </li>;
    /* jshint ignore:end */
  }
}