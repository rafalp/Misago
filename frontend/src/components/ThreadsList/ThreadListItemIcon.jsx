import React from "react"

const ThreadsListItemIcon = ({ thread }) => {
  let className = "threads-list-icon"
  if (!thread.is_read) className += " threads-list-icon-new"

  if (thread.weight === 2) {
    className += " threads-list-icon-pinned-globally"
  } else if (thread.weight === 1) {
    className += " threads-list-icon-pinned-locally"
  }

  return (
    <a
      title={getTitle(thread)}
      href={thread.is_read ? thread.url.last_post : thread.url.new_post}
      className={className}
    >
      <span className="material-icon">{getIconImage(thread)}</span>
    </a>
  )
}

const getTitle = (thread) => {
  if (!thread.is_read) {
    if (thread.weight === 2) {
      return gettext("Pinned globally (New posts)")
    } else if (thread.weight === 1) {
      return gettext("Pinned in category (New posts)")
    }
    
    return gettext("New posts")
  }

  if (thread.weight === 2) {
    return gettext("Pinned globally")
  } else if (thread.weight === 1) {
    return gettext("Pinned in category")
  }
  
  return gettext("No new posts")
}

const getIconImage = (thread) => {
  if (thread.weight === 2) {
    return "star"
  } else if (thread.weight === 1) {
    return "star_half"
  }
  
  return "chat_bubble"
}

export default ThreadsListItemIcon