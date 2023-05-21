import React from "react"

const ThreadsListItemReadStatus = ({ thread }) => {
  if (thread && !thread.is_read) {
    return (
      <div
        className="threads-list-item-read-status"
        title={pgettext("threads list", "Contains unread posts")}
      >
        <span className="threads-list-unread-icon"></span>
      </div>
    )
  }

  return (
    <div
      className="threads-list-item-read-status"
      title={pgettext("threads list", "No unread posts")}
    >
      <span className="threads-list-read-icon"></span>
    </div>
  )
}

export default ThreadsListItemReadStatus
