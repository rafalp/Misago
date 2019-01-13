import React from "react"

export default class extends React.Component {
  getHelpText() {
    if (this.props.helpText) {
      return <p className="help-block">{this.props.helpText}</p>
    } else {
      return null
    }
  }

  render() {
    return (
      <div className="panel-body panel-message-body">
        <div className="message-icon">
          <span className="material-icon">
            {this.props.icon || "info_outline"}
          </span>
        </div>
        <div className="message-body">
          <p className="lead">{this.props.message}</p>
          {this.getHelpText()}
        </div>
      </div>
    )
  }
}
