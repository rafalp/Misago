import React from "react"

export default function NotificationsListEmpty({ filter }) {
  return (
    <li className="list-group-item notifications-list-empty">
      <div className="notifications-list-empty-icon">
        <span className="material-icon">
          {filter === "unread"
            ? "sentiment_very_satisfied"
            : "notifications_none"}
        </span>
      </div>
      <p className="notifications-list-empty-message">{emptyMessage(filter)}</p>
    </li>
  )
}

function emptyMessage(filter) {
  if (filter === "read") {
    return pgettext(
      "notifications list",
      "You don't have any read notifications."
    )
  } else if (filter === "unread") {
    return pgettext(
      "notifications list",
      "You don't have any unread notifications!"
    )
  }

  return pgettext("notifications list", "You don't have any notifications.")
}
