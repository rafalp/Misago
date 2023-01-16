import React from "react"

const TYPES_CLASSES = {
  info: "alert-info",
  success: "alert-success",
  warning: "alert-warning",
  error: "alert-danger",
}

export class Snackbar extends React.Component {
  getSnackbarClass() {
    let snackbarClass = "alerts-snackbar"
    if (this.props.isVisible) {
      snackbarClass += " in"
    } else {
      snackbarClass += " out"
    }
    return snackbarClass
  }

  render() {
    return (
      <div className={this.getSnackbarClass()}>
        <p className={"alert " + TYPES_CLASSES[this.props.type]}>
          {this.props.message}
        </p>
      </div>
    )
  }
}

export function select(state) {
  return state.snackbar
}
