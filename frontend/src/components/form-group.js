import React from "react"

export default class extends React.Component {
  isValidated() {
    return typeof this.props.validation !== "undefined"
  }

  getClassName() {
    let className = "form-group"
    if (this.isValidated()) {
      className += " has-feedback"
      if (this.props.validation === null) {
        className += " has-success"
      } else {
        className += " has-error"
      }
    }
    return className
  }

  getFeedback() {
    if (this.props.validation) {
      return (
        <div className="help-block errors">
          {this.props.validation.map((error, i) => {
            return <p key={this.props.for + "FeedbackItem" + i}>{error}</p>
          })}
        </div>
      )
    } else {
      return null
    }
  }

  getFeedbackDescription() {
    if (this.isValidated()) {
      return (
        <span id={this.props.for + "_status"} className="sr-only">
          {this.props.validation
            ? pgettext("field validation status", "(error)")
            : pgettext("field validation status", "(success)")}
        </span>
      )
    } else {
      return null
    }
  }

  getHelpText() {
    if (this.props.helpText) {
      return <p className="help-block">{this.props.helpText}</p>
    } else {
      return null
    }
  }

  render() {
    return (
      <div className={this.getClassName()}>
        <label
          className={"control-label " + (this.props.labelClass || "")}
          htmlFor={this.props.for || ""}
        >
          {this.props.label + ":"}
        </label>
        <div className={this.props.controlClass || ""}>
          {this.props.children}
          {this.getFeedbackDescription()}
          {this.getFeedback()}
          {this.getHelpText()}
          {this.props.extra || null}
        </div>
      </div>
    )
  }
}
