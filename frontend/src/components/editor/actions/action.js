// jshint ignore:start
import React from 'react';

export default class extends React.Component {
  onClick = () => {
    this.props.replaceSelection(this.props.execAction);
  };

  render() {
    return (
      <button
        className={'btn btn-icon ' + this.props.className}
        disabled={this.props.disabled}
        onClick={this.onClick}
        title={this.props.title}
        type="button"
      >
        {this.props.children}
      </button>
    );
  }
}