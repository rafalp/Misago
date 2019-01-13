import React from "react"

export default class extends React.Component {
  getClassName() {
    if (this.props.dropdown) {
      return "btn btn-default btn-aligned btn-icon btn-dropdown-toggle open hidden-md hidden-lg"
    } else {
      return "btn btn-default btn-aligned btn-icon btn-dropdown-toggle hidden-md hidden-lg"
    }
  }

  render() {
    return (
      <button
        className={this.getClassName()}
        type="button"
        onClick={this.props.toggleNav}
        aria-haspopup="true"
        aria-expanded={this.props.dropdown ? "true" : "false"}
      >
        <i className="material-icon">menu</i>
      </button>
    )
  }
}
