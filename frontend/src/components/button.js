import React from "react"
import Loader from "./loader"

export default class Button extends React.Component {
  render() {
    let className = "btn " + this.props.className
    let disabled = this.props.disabled

    if (this.props.loading) {
      className += " btn-loading"
      disabled = true
    }

    return (
      <button
        className={className}
        disabled={disabled}
        onClick={this.props.onClick}
        type={this.props.onClick ? "button" : "submit"}
      >
        {this.props.children}
        {this.props.loading ? <Loader /> : null}
      </button>
    )
  }
}

Button.defaultProps = {
  className: "btn-default",

  type: "submit",

  loading: false,
  disabled: false,

  onClick: null,
}
