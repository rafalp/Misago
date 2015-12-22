import React from 'react';

export default class Button extends React.Component {
  render() {
    let content = null;
    if (this.props.loading) {
      /* jshint ignore:start */
      content = <b>loading!</b>;
      /* jshint ignore:end */
    } else {
      content = this.props.children;
    }

    /* jshint ignore:start */
    let className = 'btn ' + this.props.className;

    return <button type={this.props.type}
                   className={className}
                   disabled={this.props.disabled}
                   onClick={this.props.onClick}>
      {content}
    </button>;
    /* jshint ignore:end */
  }
}


Button.defaultProps = {
  className: "btn-default",

  type: "submit",

  loading: false,
  disabled: false,

  onClick: null
};
