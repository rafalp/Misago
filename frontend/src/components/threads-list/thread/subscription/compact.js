import React from "react"
import SubscriptionFull from "misago/components/threads-list/thread/subscription/full"
import OptionsModal from "misago/components/threads-list/thread/subscription/modal"
import modal from "misago/services/modal"

export default class extends SubscriptionFull {
  showOptions = () => {
    modal.show(<OptionsModal thread={this.props.thread} />)
  }

  render() {
    const { moderation } = this.props.thread

    let className = ""
    if (moderation.length) {
      className += "col-xs-6"
    } else {
      className += "col-xs-12"
    }
    className += " hidden-md hidden-lg"

    return (
      <div className={className}>
        <button
          type="button"
          className={this.getClassName()}
          disabled={this.props.disabled}
          onClick={this.showOptions}
        >
          <span className="material-icon">{this.getIcon()}</span>
        </button>
      </div>
    )
  }
}
