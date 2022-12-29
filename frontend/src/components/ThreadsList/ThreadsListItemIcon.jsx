import React from "react"

const ThreadsListItemIcon = ({ thread }) => {
  let className = "threads-list-icon"
  if (!thread.is_read) className += " threads-list-icon-new"

  return (
    <a
      title={thread.is_read ? gettext("No new posts") : gettext("New posts")}
      href={thread.is_read ? thread.url.last_post : thread.url.new_post}
      className={className}
    >
      <span className="material-icon">
        {thread.is_read ? "chat_bubble_outline" : "chat_bubble"}
      </span>
    </a>
  )
}

export default ThreadsListItemIcon
