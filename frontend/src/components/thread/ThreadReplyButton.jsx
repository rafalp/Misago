import React from "react"

const ThreadReplyButton = ({ onClick }) => (
  <button
    className="btn btn-primary btn-outline btn-block"
    type="button"
    onClick={onClick}
  >
    <span className="material-icon">chat</span>
    {gettext("Reply")}
  </button>
)

export default ThreadReplyButton