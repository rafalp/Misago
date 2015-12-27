import React from 'react';

const TYPES_CLASSES = {
  'info': 'alert-info',
  'success': 'alert-success',
  'warning': 'alert-warning',
  'error': 'alert-danger'
};

export class Snackbar extends React.Component {
  render() {
    var typeClass = 'alert ' + TYPES_CLASSES[this.props.type]; // jshint ignore:line

    var snackbarClass = 'alerts-snackbar';

    if (this.props.isVisible) {
      snackbarClass += ' in';
    } else {
      snackbarClass += ' out';
    }

    /* jshint ignore:start */
    return <div className={snackbarClass}>
      <p className={typeClass}>
        {this.props.message}
      </p>
    </div>;
    /* jshint ignore:end */
  }
}

export function select(state) {
  return state.snackbar;
}
