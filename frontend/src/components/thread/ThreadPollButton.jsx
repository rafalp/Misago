import classnames from "classnames"
import React from "react"

const ThreadPollButton = ({ compact, disabled, onClick }) => (
  <button
    className={classnames("btn btn-default btn-outline", {
      "btn-block": !compact,
      "btn-icon": compact,
    })}
    type="button"
    title={compact ? pgettext("thread poll btn", "Add poll") : null}
    disabled={disabled}
    onClick={onClick}
  >
    <span className="material-icon">poll</span>
    {!compact && pgettext("thread poll btn", "Add poll")}
  </button>
)

export default ThreadPollButton
