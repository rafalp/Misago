import React from 'react';
import Loader from 'misago/components/loader'; // jshint ignore:line

export default class Button extends React.Component {
  render() {
    let content = null;
    let className = 'btn ' + this.props.className;
    let disabled = this.props.disabled;

    if (this.props.loading) {
      /* jshint ignore:start */
      content = <Loader />;
      /* jshint ignore:end */
      className += ' btn-loading';
      disabled = true;
    } else {
      content = this.props.children;
    }

    /* jshint ignore:start */
    return <button type={this.props.onClick ? 'button' : 'submit'}
                   className={className}
                   disabled={disabled}
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
