import React from "react"

export default function ({ post }) {
  if (post.is_read) return null

  return (
    <div className="event-label">
      <span className="label label-unread">
        {pgettext("event unread label", "New event")}
      </span>
    </div>
  )
}
