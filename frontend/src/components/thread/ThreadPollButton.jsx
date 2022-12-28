import classnames from "classnames"
import React from "react"

const ThreadPollButton = ({ compact, onClick }) => (
  <button
    className={classnames(
      "btn btn-default btn-outline",
      {"btn-block": !compact, "btn-icon": compact}
    )}
    type="button"
    title={compact ? gettext("Add poll") : null}
    onClick={onClick}
  >
    <span className="material-icon">poll</span>
    {!compact && gettext("Add poll")}
  </button>
)

export default ThreadPollButton