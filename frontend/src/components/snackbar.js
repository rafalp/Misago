import React from 'react';

/* jshint ignore:start */
const TYPES_CLASSES = {
  'info': 'alert-info',
  'success': 'alert-success',
  'warning': 'alert-warning',
  'error': 'alert-danger'
};
/* jshint ignore:end */

export class Snackbar extends React.Component {
  getSnackbarClass() {
    let snackbarClass = 'alerts-snackbar';
    if (this.props.isVisible) {
      snackbarClass += ' in';
    } else {
      snackbarClass += ' out';
    }
    return snackbarClass;
  }

  render() {
    /* jshint ignore:start */
    return <div className={this.getSnackbarClass()}>
      <p className={'alert ' + TYPES_CLASSES[this.props.type]}>
        {this.props.message}
      </p>
    </div>;
    /* jshint ignore:end */
  }
}

export function select(state) {
  return state.snackbar;
}
