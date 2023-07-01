import React from "react"
import PanelMessage from "misago/components/panel-message"

export default class extends PanelMessage {
  getHelpText() {
    if (this.props.helpText) {
      return <p className="help-block">{this.props.helpText}</p>
    } else {
      return null
    }
  }

  render() {
    return (
      <div className="modal-body">
        <div className="message-icon">
          <span className="material-icon">
            {this.props.icon || "info_outline"}
          </span>
        </div>
        <div className="message-body">
          <p className="lead">{this.props.message}</p>
          {this.getHelpText()}
          <button
            className="btn btn-default"
            data-dismiss="modal"
            type="button"
          >
            {pgettext("modal message dismiss btn", "Ok")}
          </button>
        </div>
      </div>
    )
  }
}
