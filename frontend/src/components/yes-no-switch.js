import React from "react"

export default class extends React.Component {
  getClassName() {
    if (this.props.value) {
      return "btn btn-yes-no btn-yes-no-on"
    } else {
      return "btn btn-yes-no btn-yes-no-off"
    }
  }

  getIcon() {
    if (!!this.props.value) {
      return this.props.iconOn || "check_box"
    } else {
      return this.props.iconOff || "check_box_outline_blank"
    }
  }

  getLabel() {
    if (!!this.props.value) {
      return this.props.labelOn || pgettext("yesno switch choice", "yes")
    } else {
      return this.props.labelOff || pgettext("yesno switch choice", "no")
    }
  }

  toggle = () => {
    this.props.onChange({
      target: {
        value: !this.props.value,
      },
    })
  }

  render() {
    return (
      <button
        type="button"
        onClick={this.toggle}
        className={this.getClassName()}
        id={this.props.id || null}
        aria-describedby={this.props["aria-describedby"] || null}
        disabled={this.props.disabled || false}
      >
        <span className="material-icon">{this.getIcon()}</span>
        <span className="btn-text">{this.getLabel()}</span>
      </button>
    )
  }
}
