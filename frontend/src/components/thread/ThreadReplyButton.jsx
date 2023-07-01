import React from "react"

const ThreadReplyButton = ({ onClick }) => (
  <button
    className="btn btn-primary btn-outline btn-block"
    type="button"
    onClick={onClick}
  >
    <span className="material-icon">chat</span>
    {pgettext("thread reply btn", "Reply")}
  </button>
)

export default ThreadReplyButton
