import React from "react"
import PanelMessage from "misago/components/panel-message"

export default class extends React.Component {
  getHelpText() {
    if (this.props.options.next_on) {
      return interpolate(
        pgettext(
          "change username",
          "You will be able to change your username %(next_change)s."
        ),
        { next_change: this.props.options.next_on.fromNow() },
        true
      )
    } else {
      return pgettext(
        "change username",
        "You have changed your name allowed number of times."
      )
    }
  }

  render() {
    return (
      <div className="panel panel-default panel-form">
        <div className="panel-heading">
          <h3 className="panel-title">
            {pgettext("change username title", "Change username")}
          </h3>
        </div>
        <PanelMessage
          helpText={this.getHelpText()}
          message={pgettext(
            "change username",
            "You can't change your username at the moment."
          )}
        />
      </div>
    )
  }
}
