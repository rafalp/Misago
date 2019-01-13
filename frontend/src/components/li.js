import React from "react"

export default class extends React.Component {
  isActive() {
    if (this.props.isControlled) {
      return this.props.isActive
    } else {
      if (this.props.path) {
        return document.location.pathname.indexOf(this.props.path) === 0
      } else {
        return false
      }
    }
  }

  getClassName() {
    if (this.isActive()) {
      return (
        (this.props.className || "") +
        " " +
        (this.props.activeClassName || "active")
      )
    } else {
      return this.props.className || ""
    }
  }

  render() {
    return <li className={this.getClassName()}>{this.props.children}</li>
  }
}
